from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import IsParent
from .serializers import ParentProfileSerializer
from students.models import StudentProfile

class ParentDashboardView(APIView):
    permission_classes = [IsParent]

    def get(self, request):
        parent = request.user.parentprofile

        # 🔐 SCHOOL-SCOPED DATA PROTECTION
        children = StudentProfile.objects.filter(
            parentstudent__parent=parent,
            school=parent.school  # 👈 only children in parent’s school
        )

        data = {
            'profile': ParentProfileSerializer(parent).data,
            'children_count': children.count(),
            'school': parent.school.name
        }

        return Response(data)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from academics.models import ClassArm
from attendance.models import PhysicalAttendance
from assignments.models import Assignment
from materials.models import Material

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def parent_dashboard(request):
    parent = request.user

    if parent.role != "parent":
        return Response({"detail": "Not allowed"}, status=403)

    children = parent.children.select_related("student")

    data = []

    for link in children:
        student = link.student

        data.append({
            "student": {
                "id": student.id,
                "name": student.get_full_name(),
            },
            "classes": ClassArm.objects.filter(
                enrollments__student=student
            ).values("id", "name"),
            "attendance": PhysicalAttendance.objects.filter(
                student=student
            ).count(),
            "assignments": Assignment.objects.filter(
                classroom__enrollments__student=student
            ).count(),
            "materials": Material.objects.filter(
                classroom__enrollments__student=student
            ).count(),
        })

    return Response(data)
