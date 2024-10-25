
    $(document).ready(function(){
    $('.login-info-box').fadeOut();
    $('.login-show').addClass('show-log-panel');
});


$('.login-reg-panel input[type="radio"]').on('change', function() {
    if($('#log-login-show').is(':checked')) {
        $('.register-info-box').fadeOut();
        $('.login-info-box').fadeIn();

        $('.white-panel').addClass('right-log');
        $('.register-show').addClass('show-log-panel');
        $('.login-show').removeClass('show-log-panel');

    }
    else if($('#log-reg-show').is(':checked')) {
        $('.register-info-box').fadeIn();
        $('.login-info-box').fadeOut();

        $('.white-panel').removeClass('right-log');

        $('.login-show').addClass('show-log-panel');
        $('.register-show').removeClass('show-log-panel');
    }
});













///* scripts.js */
//let actionType;
//let itemId;
//
//function openModal(action, id) {
//  actionType = action;
//  itemId = id;
//  const modal = document.getElementById('confirmationModal');
//  const message = action === 'delete' ? 'Are you sure you want to delete this item?' : 'Are you sure you want to edit this item?';
//  document.getElementById('modalMessage').innerText = message;
//  modal.style.display = 'block';
//}
//
//function closeModal() {
//  document.getElementById('confirmationModal').style.display = 'none';
//}
//
//function confirmAction() {
//  if (actionType === 'delete') {
//    // Perform delete action
//    alert(`Item ${itemId} deleted!`);
//  } else if (actionType === 'edit') {
//    // Perform edit action
//    alert(`Item ${itemId} edited!`);
//  }
//  closeModal();
//}
//
//// Close the modal when clicking outside of it
//window.onclick = function(event) {
//  const modal = document.getElementById('confirmationModal');
//  if (event.target == modal) {
//    modal.style.display = 'none';
//  }
//}



//
//function confirmDelete(element) {
//    var modal = document.getElementById('deleteModal');
//    var confirmBtn = document.getElementById('confirmDeleteBtn');
//    var itemId = element.getAttribute('data-id');
//
//    modal.style.display = 'block';
//
//    confirmBtn.onclick = function() {
//        // Send the ID to the backend
//        fetch('/delete', {
//            method: 'POST',
//            headers: {
//                'Content-Type': 'application/json'
//            },
//            body: JSON.stringify({ id: itemId })
//        })
//        .then(response => response.json())
//        .then(data => {
//            console.log('Success:', data);
//            // Close the modal and refresh the page or update the table
//            modal.style.display = 'none';
//            location.reload();
//        })
//        .catch((error) => {
//            console.error('Error:', error);
//        });
//    };
//}
//
//function closeModal() {
//    var modal = document.getElementById('deleteModal');
//    modal.style.display = 'none';
//}
//
//// Close the modal when clicking outside of it
//window.onclick = function(event) {
//    var modal = document.getElementById('deleteModal');
//    if (event.target == modal) {
//        modal.style.display = 'none';
//    }
//}






function confirmDelete(element) {
    var modal = document.getElementById('deleteModal');
    var confirmBtn = document.getElementById('confirmDeleteBtn');
    var itemId = element.getAttribute('data-id');


    modal.style.display = 'block';

    confirmBtn.onclick = function() {
        // Send the ID to the backend for deletion
        fetch('/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: itemId })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            modal.style.display = 'none';
            location.reload();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    };
}







function confirmEdit(element) {
    var modal = document.getElementById('editModal');
    var confirmBtn = document.getElementById('confirmEditBtn');
    var itemId = element.getAttribute('data-id');


    modal.style.display = 'block';

    confirmBtn.onclick = function() {
        // Send the ID to the backend for edition
        fetch('/table', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: itemId })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            modal.style.display = 'none';

        })
        .catch((error) => {
            console.error('Error:', error);
        });
    };
}

function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = 'none';
}

// Close the modal when clicking outside of it
window.onclick = function(event) {
    var deleteModal = document.getElementById('deleteModal');
    var editModal = document.getElementById('editModal');
    if (event.target == deleteModal) {
        deleteModal.style.display = 'none';
    }
    if (event.target == editModal) {
        editModal.style.display = 'none';
    }
}





