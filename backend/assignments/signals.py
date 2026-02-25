from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Assignment
from notifications.utils import notify_students

@receiver(post_save, sender=Assignment)
def assignment_created_notification(sender, instance, created, **kwargs):
    if created:
        students = instance.classroom.students.all()  # assumes Classroom has 'students' related_name
        notify_students(
            users=students,
            title="New Assignment",
            message=f"A new assignment '{instance.title}' has been posted.",
            notification_type="assignment",
            delivery_channel="push"
        )
