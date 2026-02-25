from django.db import models
from django.conf import settings
from assignments.models import Assignment 

class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions_submissions"  # unique reverse accessor
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # ✅ comma was missing here
        related_name="submissions_submissions"  # unique reverse accessor
    )
    
    answer_text = models.TextField(blank=True)
    file = models.FileField(
        upload_to="submissions/",
        blank=True,
        null=True
    )
    score = models.FloatField(blank=True, null=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ("assignment", "student")

    def __str__(self):
        return f"{self.student} → {self.assignment}"

