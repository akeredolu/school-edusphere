from django.db import models

# -------------------
# Academic Classes
# -------------------
class AcademicClass(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # JSS1, SS2
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.school.name})"


class ClassArm(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE)
    academic_class = models.ForeignKey(
        AcademicClass,
        on_delete=models.CASCADE,
        related_name='arms'
    )
    name = models.CharField(max_length=50)  # A, B, Science

    def __str__(self):
        return f"{self.academic_class.name} {self.name} ({self.school.name})"


# -------------------
# Subjects
# -------------------
class Subject(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.school.name})"


# -------------------
# Enrollment
# -------------------
class Enrollment(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE)
    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE
    )
    class_arm = models.ForeignKey(
        ClassArm,
        on_delete=models.CASCADE
    )
    academic_session = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.class_arm}"


# -------------------
# Teacher Subjects
# -------------------
class TeacherSubject(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        'teachers.TeacherProfile',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )
    class_arm = models.ForeignKey(
        ClassArm,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.teacher.user.username} - {self.subject.name} ({self.school.name})"

