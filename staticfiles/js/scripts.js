window.onload = function() {
    calculateSubtotals();

};

document.addEventListener("DOMContentLoaded", function() {
    calculateTotal();
});


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');


function calculateSubtotals() {
    var cartItems = document.querySelectorAll('.flex-item');
    var total = 0;
    cartItems.forEach(function(cartItem) {
        var price = parseFloat(cartItem.querySelector('.price').getAttribute('data-price'));
        var quantity = parseInt(cartItem.querySelector('.quantity').getAttribute('data-quantity'));
        var subtotal = price * quantity;
        cartItem.querySelector('.subtotal').textContent ='Subtotel: ' + subtotal.toFixed(2);
        
        total += subtotal;
    });
    return total.toFixed(2);
}


function calculateTotal() {

    var total = calculateSubtotals(); // Get the total from calculateSubtotals function
    console.log("Total:", total);

    var totalElement = document.getElementById('total-amount');
    console.log(totalElement)
    if (totalElement) {
        totalElement.textContent = 'Total Amount: ' + total;
    } else {
        console.error('Total element not found.');
    }
}




document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelectorAll('.add-btn, .remove-btn, .delete-btn').forEach(function(element) {
        element.addEventListener('click', function(event) {
            event.preventDefault();  // Prevent the default action (navigation)

            var quantityElement = element.parentElement.parentElement.querySelector('.quantity');
            // console.log(quantityElement);
            // console.log(element.parentElement);
            var quantity = parseInt(quantityElement.getAttribute('data-quantity'));
            // console.log(element.parentElement.innerHTML);
            // console.log(quantity);
            var url;
            var itemId = element.parentElement.parentElement.getAttribute('data-item-id');

            if (element.classList.contains('add-btn')) {
                quantity++;
                url = '/add_to_cart/' + itemId + '/';
            } else if (element.classList.contains('remove-btn')) {
                quantity = Math.max(0, quantity - 1);  // Ensure quantity doesn't go below 0
                console.log(itemId)
                url = '/decrement_cart/' + itemId + '/';
            } else if (element.classList.contains('delete-btn')) {
                url = '/remove_from_cart/' + itemId + '/';
            }

            quantityElement.setAttribute('data-quantity', quantity);
            quantityElement.textContent = 'Quantity: ' + quantity;

            calculateSubtotals();

            // Make a POST request to the server to update the quantity in the database
            var xhr = new XMLHttpRequest();
            xhr.open('POST', url, true);
            xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
            xhr.send('quantity=' + encodeURIComponent(quantity));
            xhr.onload = function() {
                if (xhr.status == 200) {
                    location.reload();
                }
            }
            

        });
    });
});


