from django.core.mail import EmailMessage

def send_payment_receipt(email, invoice):
    mail = EmailMessage(
        subject="Payment Receipt",
        body=f"Payment received for {invoice.term}",
        to=[email],
    )
    mail.send()

