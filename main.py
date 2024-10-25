import datetime
import os

import mysql
from flask import Flask, url_for, request, abort, flash, render_template, redirect, jsonify
from flask_login import UserMixin, login_user, LoginManager, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy import select, String, Float, Integer, Date, Column, func, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import calendar
from datetime import datetime as dt
import pandas as pd
import mysql.connector
import mysql.connector.cursor
from mysql.connector import Error

app = Flask(__name__)



app.config["SECRET_KEY"] = 'Reza123456789'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@host:port/database
# f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', "sqlite:///contas.db")


db = SQLAlchemy()
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


Bootstrap(app)


class Item(UserMixin, db.Model):
    __tablename__ = "items_table"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    user = relationship('User', back_populates='item')
    item_name = db.Column(db.String(80), nullable=False)
    item_month = db.Column(db.String(80), nullable=False)
    item_data_add = db.Column(db.DateTime, server_default=func.now())
    item_data_edit = db.Column(db.DateTime, server_default=func.now(), onupdate=True)
    item_price = db.Column(Float, nullable=False)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(Integer, ForeignKey('items_table.id'))
    item = relationship('Item', back_populates='user')
    f_name = db.Column(db.String(80), nullable=False)
    l_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def entry():
    # if request.method == 'POST':
    #
    #     # try:
    #     #     pdt_to_del = db.session.execute(db.select(Product).where(Product.pdt_name.like('Ni%'))).scalar()
    #     # except IndexError:
    #     #     flash('There is nothing here')
    #     #     return redirect(url_for('home'))
    #     # db.session.delete(pdt_to_del)
    #     # db.session.commit()
    #
    #     pdt_to_del = db.session.execute(db.select(Item).where(Item.pdt_name.like(f'%{request.form['itm_name']}%'))).scalars().all()
    #     if request.form['itm_name'] == "":
    #         #will consider as space and will show everything so i put [] to empty it
    #         pdt_to_del = []
    #         flash(f' Please write down ')
    #     elif not pdt_to_del :
    #         flash(f' Could not find anything by {request.form['itm_name']} ')
    #
    #
    #     # for item in pdt_to_del:
    #     #     print(item.pdt_name)
    #     # return redirect(url_for('home'))
    #     return render_template('index.html', items=pdt_to_del)
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['login-email']
        password = request.form['login-password']
        user = db.session.execute(db.Select(User).where(User.email == email)).scalar()
        if not user:
            flash('There is not such Email.')
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('* Password is wrong!!!')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html', logged_in=current_user.is_authenticated)


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        if request.form['register-password'] == request.form['register-password-confirm']:
            new_user = User(
                f_name=request.form['fname'],
                l_name=request.form['lname'],
                email=request.form['register-email'],
                password=generate_password_hash(password=request.form['register-password'], method="pbkdf2:sha256",
                                                salt_length=16)
            )

            result = db.session.execute(db.select(User).where(User.email == new_user.email))
            user = result.scalar()
            if user:
                flash(f"*{user.email}*")
                flash("already exist. Log In instead!")
                return redirect(url_for('login'))
            else:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('home'))
        else:
            flash("please confirm the password again!")
            return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('entry'))
    query = db.session.execute(db.select(Item).where(Item.item_month == dt.now().strftime('%Y-%m'))).scalars()
    prices = [item.item_price for item in query]
    months = [month for month in calendar.month_name]

    if request.method == "POST":

        action = request.form['submit']

        if action == 'Add':
            if request.form['month'] == "" or request.form['price'] == "R$ " or request.form['item'] == "":
                flash('Fill the form please!!!')
                return redirect(url_for('home'))
            else:
                new_item = Item(
                    item_month=request.form['month'],
                    item_price=pd.to_numeric(request.form['price'][3:]),
                    item_name=request.form['item'],
                    user_id=current_user.id
                )
                db.session.add(new_item)
                db.session.commit()

        elif action == 'Total':
            total = sum(prices)
            return render_template('app_page.html', months=months[1:], date=dt, total=total, is_total=True)
        elif action == 'Details':
            return redirect(url_for('details'))
        elif action == 'Exit':
            return redirect(url_for('logout'))
    return render_template('app_page.html', months=months[1:], date=dt)


@app.route('/open-calculator')
def open_calculator():
    os.system('calc.exe')
    return "Calculator opened"

@app.route('/table', methods=['GET', 'POST'])
def details():
    if not current_user.is_authenticated:
        return redirect(url_for('entry'))
    data = db.session.execute(db.select(Item)).scalars().all()
    if request.method == 'POST':
        item_id = int(request.form['id'])
        name = request.form['name']
        month = request.form['month']
        price = request.form['price']

        # Handle your data here, e.g., update your database
        print(f'Item ID: {item_id}, Name: {name}, Month: {month}, Price: {price}')
        item_to_edit = db.session.execute(db.select(Item).where(Item.id == item_id)).scalar_one()

        item_to_edit.user_id = current_user.id
        item_to_edit.item_name = name
        item_to_edit.item_month = month
        item_to_edit.item_price = price
        item_to_edit.item_data_edit = datetime.datetime.now()

        db.session.commit()
        return render_template('details_table.html', data=data)
    else:
        # pagination without jquery
        # data = db.session.execute(db.select(Item)).scalars().all()
        # page = request.args.get('page', 1, type=int)
        # per_page = 28
        # total = len(data)
        # pages = math.ceil(total / per_page)  # ceil func will round the number up 2.1 = 3
        # start = (page - 1) * per_page
        # end = start + per_page
        # paginated_data = data[start:end]

        # , data = paginated_data, page = page, pages = pages
        if request.args.get('id'):
            item = Item.query.get_or_404(request.args.get('id'))
            print(item.item_price)
            return render_template('details_table.html', data=data, is_for_edit=True, selected_id=int(request.args.get('id')))
    return render_template('details_table.html', data=data)


@app.route('/delete', methods=['POST'])
def delete_item():
    selected_id = request.get_json()
    item_id = selected_id['id']
    item_to_del = db.get_or_404(Item, item_id)
    db.session.delete(item_to_del)
    db.session.commit()
    print(item_id)
    return jsonify({'message': 'Item deleted successfully'})


@app.route('/edit', methods=['POST'])
def submit():
    if request.method == 'POST':
        print(request.args.get('data-id'))
        return render_template('details_table.html')
    # data = request.json
    # form = data.get('formData')
    #
    # print(form['item_name'], form['item_price'], form['item_month'])
    # # Process the data as needed
    # return jsonify({'status': 'success', 'data': data})
    return render_template('details_table.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('entry'))



if __name__ == '__main__':
    app.run(port=5003, debug=True)
