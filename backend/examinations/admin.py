from django.contrib import admin
from .models import Exam, Question, Option, StudentExam, StudentAnswer

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'class_arm', 'school', 'start_time', 'end_time', 'is_published')
    search_fields = ('title', 'subject__name')
    list_filter = ('class_arm', 'school', 'subject', 'is_published')
    ordering = ('-start_time',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'exam', 'marks')
    search_fields = ('text',)
    list_filter = ('exam',)
    ordering = ('exam',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    list_filter = ('question', 'is_correct')


@admin.register(StudentExam)
class StudentExamAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'score', 'started_at', 'submitted_at')
    search_fields = ('student__user__username', 'exam__title')
    list_filter = ('exam', 'started_at')
    ordering = ('-started_at',)


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('student_exam', 'question', 'selected_option')
    list_filter = ('student_exam', 'question')
