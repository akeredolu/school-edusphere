from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Material
from notifications.utils import notify_students

@receiver(post_save, sender=Material)
def material_uploaded_notification(sender, instance, created, **kwargs):
    if created:
        students = instance.classroom.students.all()
        notify_students(
            users=students,
            title="New Material Available",
            message=f"New material '{instance.title}' has been uploaded.",
            notification_type="material",
            delivery_channel="push"
        )

