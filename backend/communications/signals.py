# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from academics.models import ClassArm
from communications.models import Conversation

@receiver(post_save, sender=ClassArm)
def create_class_chat(sender, instance, created, **kwargs):
    if created:
        conversation = Conversation.objects.create(is_group=True)
        participants = [teacher.user for teacher in instance.teachers.all()]
        participants += [enrollment.student.user for enrollment in instance.enrollment_set.all()]
        conversation.participants.set(participants)

