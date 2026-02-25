# backend/academics/admin.py
from django.contrib import admin
from .models import ClassArm, Subject

@admin.register(ClassArm)
class ClassArmAdmin(admin.ModelAdmin):
    list_display = ('name', 'school')
    search_fields = ('name',)
    list_filter = ('school',)
    ordering = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'school')
    search_fields = ('name', 'code')
    list_filter = ('school',)
    ordering = ('name',)

