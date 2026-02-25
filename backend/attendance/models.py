from django.db import models
from django.conf import settings
from students.models import StudentProfile
import uuid

class Guardian(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="guardians/")
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()

class StudentGuardian(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    relationship = models.CharField(max_length=50)  # Father, Mother, Uncle

class PhysicalAttendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in_time = models.DateTimeField(null=True, blank=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("present", "Present"), ("absent", "Absent")]
    )

class PickupCode(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)
