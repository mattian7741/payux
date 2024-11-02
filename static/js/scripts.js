document.addEventListener('DOMContentLoaded', function () {
    const donateButtons = document.querySelectorAll('.donate-btn');
    const otherButton = document.getElementById('other-btn');
    const otherModal = document.getElementById('other-amount-modal');
    const otherAmountInput = document.getElementById('other-amount');
    const submitOtherAmount = document.getElementById('submit-other-amount');

    // Handle predefined donation amounts
    donateButtons.forEach(button => {
        button.addEventListener('click', function () {
            const amount = this.getAttribute('data-amount');
            createCheckoutSession(amount);
        });
    });

    // Show modal for "Other" donation
    otherButton.addEventListener('click', function () {
        otherModal.style.display = 'block';
    });

    // Submit the custom amount
    submitOtherAmount.addEventListener('click', function () {
        const customAmount = otherAmountInput.value;
        if (customAmount && customAmount > 0) {
            createCheckoutSession(customAmount);
        }
    });

    // Function to create checkout session
    function createCheckoutSession(amount) {
        fetch('/create-checkout-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ amount: amount })
        })
        .then(response => response.json())
        .then(data => {
            if (data.sessionId) {
                // Redirect to the payment page using the session ID
                window.location.href = `/checkout/${data.sessionId}`;
            } else {
                alert('Error creating checkout session. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});
