from django.contrib import admin
from .models import LearningMaterial, Assignment, AssignmentSubmission

@admin.register(LearningMaterial)
class LearningMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'class_arm', 'school', 'created_at')
    search_fields = ('title', 'teacher__username', 'class_arm__name')
    list_filter = ('class_arm', 'school', 'teacher')
    ordering = ('-created_at',)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'class_arm', 'school', 'due_date', 'created_at')
    search_fields = ('title', 'teacher__username', 'class_arm__name')
    list_filter = ('class_arm', 'school', 'teacher')
    ordering = ('-created_at',)


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'score', 'submitted_at')
    search_fields = ('assignment__title', 'student__user__username')
    list_filter = ('assignment', 'submitted_at')
    ordering = ('-submitted_at',)
