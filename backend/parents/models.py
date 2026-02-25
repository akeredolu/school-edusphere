# parents/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from schools.models import School
# Use string reference for StudentProfile to avoid import issues
# from students.models import StudentProfile  # not needed because we use string reference

class ParentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='parents')
    phone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='parents/photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class ParentStudent(models.Model):
    parent = models.ForeignKey(
        'parents.ParentProfile',  # string reference works safely
        on_delete=models.CASCADE,
        related_name='children_links'  # unique reverse accessor
    )
    student = models.ForeignKey(
        'students.StudentProfile',  # string reference
        on_delete=models.CASCADE,
        related_name='parent_links'  # unique reverse accessor
    )

    class Meta:
        unique_together = ('parent', 'student')  # prevent duplicates

    def __str__(self):
        return f"{self.parent.user.username} -> {self.student.user.username}"

