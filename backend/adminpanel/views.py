from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.permissions import IsAdminUserRole
from students.models import StudentProfile
from academics.models import AcademicClass
from attendance.models import PhysicalAttendance

@api_view(["GET"])
@permission_classes([IsAdminUserRole])
def admin_overview(request):
    return Response({
        "users": StudentProfile.objects.count(),
        "students": StudentProfile.objects.filter(role="student").count(),
        "teachers": StudentProfile.objects.filter(role="teacher").count(),
        "classes": AcademicClass.objects.count(),
        "attendance_records": PhysicalAttendance.objects.count()
    })


@api_view(["GET"])
@permission_classes([IsAdminUserRole])
def admin_users(request):
    users = User.objects.all().order_by("-date_joined")
    return Response([
        {
            "id": u.id,
            "name": u.get_full_name(),
            "email": u.email,
            "role": u.role,
            "active": u.is_active
        } for u in users
    ])
