import pandas
import mysql.connector
from mysql.connector import Error
import os


class Connecting:
    def __init__(self):
        pw = os.environ.get("DB_PW")
        db = 'PrestacaoDeCompras'
        self.connection = self.create_server_connection('127.0.0.1', 'root', pw)
        self.create_database_query = f"""create database {db}"""
        self.create_database(self.connection, self.create_database_query)
        self.create_database_connection('127.0.0.1', 'root', pw, db)

    def create_server_connection(self, host, user, password):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            print('MySql is connecting')
        except Error as err:
            print(f"Error: {err}")
        return connection


    # connection = create_server_connection('127.0.0.1', 'root', pw)


    def create_database(self, connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            print("Database was created")
        except Error as err:
            print(f'Error: {err}')


    # create_database_query = f"""create database {db}"""
    #
    # create_database(connection, create_database_query)


    def create_database_connection(self, host, user, password, database):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            print("Database is connecting")
        except Error as err:
            print(f"Error: {err}")
        return connection


    # create_database_connection('127.0.0.1', 'root', pw, db)

    #
    # def query_execute(connection, query):
    #     cursor = connection.cursor()
    #     try:
    #         cursor.execute(query)
    #         connection.commit()
    #         print("query has been successfully commited")
    #     except Error as err:
    #         print(f"Error: {err}")
    #
    #
    # create_table = f"""
    # Create table Users(
    # user_id int auto_increment primary key,
    # fname varchar(80) not null,
    # lname varchar(80) not null,
    # age int not null,
    # email varchar(100) not null unique,
    # password varchar(30) not null,
    # created_at timestamp  default current_timestamp
    # );
    # insert into Users(fname,lname,age,email,password) values(
    # 'Reza','Foroutan' 'manesh',33,'mr.forutan2017@gmail.com','reza123'
    # )
    # """
    # connection = create_database_connection('127.0.0.1', 'root', pw, db)
    # q2 = """insert into Users(fname,lname,age,email,password) values(
    # 'Niousha','Foroutan manesh',24,'mr.forutan2020@gmail.com','reza123')"""
    # query_execute(connection, q2)
    #
    #
    # def read_query():
    #     pass
