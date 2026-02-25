# notifications/services.py
def send_sms(phone, message):
    """
    Replace internals with any provider
    """
    print(f"SMS to {phone}: {message}")
    return True

def notify_wrong_code(student, attempted_code):
    message = (
        f"ALERT: Invalid pickup code attempt for {student.full_name}."
    )

    for guardian in student.guardians.all():
        send_sms(guardian.phone, message)
