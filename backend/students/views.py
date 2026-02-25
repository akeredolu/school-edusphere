from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import IsStudent
from .serializers import StudentProfileSerializer

class StudentDashboardView(APIView):
    permission_classes = [IsStudent]

    def get(self, request):
        student = request.user.studentprofile

        # 🔐 SCHOOL-SCOPED DATA PROTECTION
        # Not needed here because 'student' is already a single object,
        # but if you were fetching multiple students, you would do:
        # students = StudentProfile.objects.filter(school=request.user.school)

        data = {
            'profile': StudentProfileSerializer(student).data,
            'school': student.school.name,
            'message': 'Welcome to your dashboard'
        }

        return Response(data)

