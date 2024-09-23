from flask import request, jsonify, Blueprint
import requests
from app.v1 import db

from app.v1.utils.token_manager import token_required

payment = Blueprint(import_name=__name__, name="payment")



@payment.route('/payment-callback', methods=['GET'])
def payment_callback():
    """handles payment"""

    reference = request.args.get('reference')

    if not reference:
        return jsonify({"No reference provided"}), 400

    # Verify User payment
    response = requests.get(f'https://api.paystack.co/transaction/verify/{reference}', 
                            headers={'Authorization': f"Bearer {os.getenv('PAYSTACK_SECRET_KEY')}"})

    if response.status_code == 200:

        data = response.json().get('data', {})
        status = data.get('status')
        if status == 'success':
            customer = data.get('customer', {})
            email = customer.get('email')
            if email:

                # Update user's payment status in the database
                #user = PaymentStatus.query.filter_by(email=email).first()
                if user:
                    user.is_paid = True
                    db.session.commit()
                    return redirect(url_for('pages.register_applicant'))
                else:
                    return "User not found", 400
            else:
                return "Email not found in Paystack response", 400
        else:
            return f"Payment verification failed: {status}", 400
    else:
        return "Failed to verify payment with Paystack", 400
