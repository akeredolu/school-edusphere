# virtual_classroom/admin.py
from django.contrib import admin
from .models import VirtualClass, VirtualAttendance
from .models import ClassRecording

admin.site.register(VirtualClass)
admin.site.register(VirtualAttendance)
admin.site.register(ClassRecording)