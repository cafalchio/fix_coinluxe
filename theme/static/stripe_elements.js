/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment

    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

var stripePublicKey = document.getElementById('id_stripe_public_key').textContent;
var clientSecret = document.getElementById('id_client_secret').textContent;

// Create a Stripe client
var stripe = Stripe(stripePublicKey);

// Create an instance of Elements
var elements = stripe.elements();

// Create a card element and mount it to the card element container
var cardElement = elements.create('card');
cardElement.mount('#card-element');

// Handle the form submission
var form = document.getElementById('payment-form');
var cardButton = document.getElementById('card-button');

form.addEventListener('submit', function(event) {
    event.preventDefault();
    cardButton.disabled = true;

    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: cardElement,
            billing_details: {
                // Include any additional billing details if required
            }
        }
    }).then(function(result) {
        if (result.error) {
            // Handle errors
            var errorElement = document.getElementById('card-errors');
            errorElement.textContent = result.error.message;
            cardButton.disabled = false;
        } else {
            // Payment succeeded
            form.submit();
        }
    });
});