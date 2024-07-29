window.onload = function() {
    calculateSubtotals();
    calculateTotal();
};
// var csrftoken = document.cookie.split('; ').find(row => row.startsWith('csrftoken')).split('=')[1];
// xhr.setRequestHeader('X-CSRFToken', csrftoken);

xhr.onload = function() {
    if (xhr.status == 200) {
        console.log("The quantity was updated successfully")
    } else {
        console.log("quantity updation failed")
    }
};

function calculateSubtotals() {
    var cartItems = document.querySelectorAll('.flex-item');
    
    cartItems.forEach(function(cartItem) {
        var price = parseFloat(cartItem.querySelector('.price').getAttribute('data-price'));
        var quantity = parseInt(cartItem.querySelector('.quantity').getAttribute('data-quantity'));
        var subtotal = price * quantity;
        cartItem.querySelector('.subtotal span').textContent = subtotal.toFixed(2);

    });
}

function calculateTotal() {
    var subtotals = document.querySelectorAll('.subtotal');
    var total = 0;

    subtotals.forEach(function(subtotal) {
        total += parseFloat(subtotal.textContent);
    });

    document.getElementById('total').textContent = total.toFixed(2);
}



document.querySelectorAll('.add-btn, .remove-btn').forEach(function(element) {
    element.addEventListener('click', function(event) {
        event.preventDefault();  // Prevent the default action (navigation)

        var quantityElement = element.parentElement.querySelector('.quantity');
        var quantity = parseInt(quantityElement.getAttribute('data-quantity'));

        var url;
        if (element.classList.contains('add-btn')) {
            quantity++;
            url = '/addtocart/' + encodeURIComponent(element.getAttribute('data-item-id')) + '/';
        } else if (element.classList.contains('remove-btn')) {
            quantity = Math.max(0, quantity - 1);  // Ensure quantity doesn't go below 0
            url = '/decrement_cart/' + encodeURIComponent(element.getAttribute('data-item-id')) + '/';
        }

        quantityElement.setAttribute('data-quantity', quantity);
        quantityElement.textContent = 'Quantity: ' + quantity;

        calculateSubtotals();
        calculateTotal();

        // Make a POST request to the server to update the quantity in the database
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send('quantity=' + encodeURIComponent(quantity));
    });
});
