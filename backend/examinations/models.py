from django.db import models

from django.db import models

class Exam(models.Model):
    school = models.ForeignKey('schools.School', on_delete=models.CASCADE)
    class_arm = models.ForeignKey('academics.ClassArm', on_delete=models.CASCADE)
    subject = models.ForeignKey('academics.Subject', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    duration_minutes = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    marks = models.PositiveIntegerField()

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

class StudentExam(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

class StudentAnswer(models.Model):
    student_exam = models.ForeignKey(StudentExam, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)


from django.db import models
from django.conf import settings
from academics.models import ClassArm
from .models import Exam, StudentExam

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="results")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassArm, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    taken_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("exam", "student")  # prevent duplicate results

    def __str__(self):
        return f"{self.student.get_full_name()} - {self.exam.title} ({self.score})"

    @classmethod
    def create_from_student_exam(cls, student_exam: StudentExam):
        """
        Utility to convert StudentExam to ExamResult
        """
        return cls.objects.create(
            exam=student_exam.exam,
            student=student_exam.student.user,  # adjust if student has user FK
            classroom=student_exam.exam.class_arm,
            score=student_exam.score
        )
