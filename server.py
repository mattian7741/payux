from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import stripe
import os

app = Flask(__name__)
CORS(app)

# Load Stripe API key from file or environment variable
try:
    with open("stripe_key.key", "r") as key_file:
        stripe.api_key = key_file.read().strip()
except FileNotFoundError:
    stripe.api_key = os.getenv("STRIPE_KEY")
    if stripe.api_key is None:
        raise ValueError("Stripe API key not found in file or environment variable.")


@app.route('/index')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/')
def serve_wheel():
    return send_from_directory('.', 'wheel.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        data = request.get_json()
        amount = data.get('amount', 0)
        print("Received amount:", amount)  # Debug: print received amount

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Investment in Project XYZ',
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:5500/success.html',
            cancel_url='http://localhost:5500/cancel.html',
        )
        print("Session created successfully:", session)  # Debug: print session data
        return jsonify(id=session.id)
    except Exception as e:
        print("Error creating checkout session:", e)  # Debug: print error message
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8500, debug=True)
