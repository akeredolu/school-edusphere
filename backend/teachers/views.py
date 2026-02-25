from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import IsTeacher
from .serializers import TeacherProfileSerializer

class TeacherDashboardView(APIView):
    permission_classes = [IsTeacher]

    def get(self, request):
        teacher = request.user.teacherprofile

        data = {
            'profile': TeacherProfileSerializer(teacher).data,
            'school': teacher.school.name,
            'message': 'Teacher dashboard loaded'
        }

        return Response(data)
