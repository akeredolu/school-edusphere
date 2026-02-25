from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Class(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="classes")
    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class ClassSession(models.Model):
    classroom = models.ForeignKey(Class, on_delete=models.CASCADE, related_name="sessions")
    topic = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    meeting_link = models.URLField(blank=True)

    def __str__(self):
        return self.topic

class Enrollment(models.Model):
    classroom = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("classroom", "student")

    def __str__(self):
        return f"{self.student} → {self.classroom}"
