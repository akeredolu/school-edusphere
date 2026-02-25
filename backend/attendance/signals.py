from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PhysicalAttendance
from notifications.utils import notify_students

@receiver(post_save, sender=PhysicalAttendance)
def attendance_marked_notification(sender, instance, created, **kwargs):
    if created:
        students = instance.classroom.students.all()
        notify_students(
            users=students,
            title="Attendance Update",
            message=f"Your attendance for {instance.date} has been recorded.",
            notification_type="attendance",
            delivery_channel="push"
        )

