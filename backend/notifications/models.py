from django.db import models
from django.conf import settings


class Notification(models.Model):
    # What the notification is about (business context)
    NOTIFICATION_TYPES = (
        ("system", "System"),
        ("assignment", "Assignment"),
        ("attendance", "Attendance"),
        ("material", "Material"),
    )

    # How the notification is delivered
    DELIVERY_CHANNELS = (
        ("sms", "SMS"),
        ("email", "Email"),
        ("push", "Push"),
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    title = models.CharField(max_length=255)
    message = models.TextField()

    # Business meaning
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )

    # Delivery method
    delivery_channel = models.CharField(
        max_length=10,
        choices=DELIVERY_CHANNELS
    )

    # Status flags
    is_sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient} — {self.title} ({self.notification_type})"

