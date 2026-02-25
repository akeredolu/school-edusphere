from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "recipient",
        "title",
        "notification_type",
        "delivery_channel",
        "is_read",
        "is_sent",
        "created_at",
    )

    list_filter = (
        "notification_type",
        "delivery_channel",
        "is_read",
        "is_sent",
    )

    search_fields = ("title", "message", "recipient__email")
    ordering = ("-created_at",)
