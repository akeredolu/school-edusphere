from django.contrib import admin
from .models import Guardian, StudentGuardian, PhysicalAttendance, PickupCode

admin.site.register(Guardian)
admin.site.register(StudentGuardian)
admin.site.register(PhysicalAttendance)
admin.site.register(PickupCode)
