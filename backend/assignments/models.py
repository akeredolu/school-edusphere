# assignments/models.py
from django.db import models
from django.conf import settings
from academics.models import ClassArm

class Assignment(models.Model):
    classroom = models.ForeignKey(
        ClassArm,
        on_delete=models.CASCADE,
        related_name="assignments"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    total_marks = models.PositiveIntegerField(default=100)
    attachment = models.FileField(
        upload_to="assignments/",
        blank=True,
        null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="assignment_submissions" 
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assignment_submissions"  # unique name
    )
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="submissions/", blank=True, null=True)
    marks_obtained = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.assignment.title}"
