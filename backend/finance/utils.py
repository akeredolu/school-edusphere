import requests
from django.conf import settings

PAYSTACK_SECRET = settings.PAYSTACK_SECRET_KEY

def initialize_paystack_payment(email, amount, reference):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {"Authorization": f"Bearer {PAYSTACK_SECRET}"}
    data = {
        "email": email,
        "amount": int(amount * 100),  # Paystack expects kobo
        "reference": reference
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

