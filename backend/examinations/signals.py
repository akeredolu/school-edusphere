from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentExam, ExamResult

@receiver(post_save, sender=StudentExam)
def create_exam_result(sender, instance, created, **kwargs):
    """
    Automatically create ExamResult when a StudentExam is submitted.
    """
    # Only create ExamResult if StudentExam has been submitted
    if instance.submitted_at and not ExamResult.objects.filter(exam=instance.exam, student=instance.student.user).exists():
        ExamResult.objects.create(
            exam=instance.exam,
            student=instance.student.user,  # adjust if student has user FK
            classroom=instance.exam.class_arm,
            score=instance.score
        )

