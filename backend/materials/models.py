from django.db import models
from django.conf import settings

class LearningMaterial(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE)
    teacher = models.ForeignKey('teachers.TeacherProfile', on_delete=models.CASCADE)
    class_arm = models.ForeignKey('academics.ClassArm', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='materials/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE)
    teacher = models.ForeignKey('teachers.TeacherProfile', on_delete=models.CASCADE)
    class_arm = models.ForeignKey('academics.ClassArm', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE)
    file = models.FileField(upload_to='submissions/')
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)


class Material(models.Model):
    MATERIAL_TYPES = (
        ("pdf", "PDF"),
        ("video", "Video"),
        ("link", "External Link"),
        ("file", "File"),
        ("note", "Note"),
    )

    classroom = models.ForeignKey(
        "academics.ClassArm",
        on_delete=models.CASCADE,
        related_name="materials"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPES)
    file = models.FileField(
        upload_to="materials/",
        blank=True,
        null=True
    )
    external_url = models.URLField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
