# attendance/services.py
from notifications.services import send_sms
from notifications.models import Notification

def notify_pickup(student, guardian):
    message = (
        f"{student.full_name} has been picked up successfully "
        f"by {guardian.full_name} at {timezone.now().strftime('%H:%M')}."
    )

    send_sms(guardian.phone, message)

    Notification.objects.create(
        user=guardian.user,
        title="Student Pickup Confirmation",
        message=message,
        notification_type="sms",
        is_sent=True
    )



