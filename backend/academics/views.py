from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsSchoolAdmin
from .models import AcademicClass, Subject
from .serializers import AcademicClassSerializer, SubjectSerializer


class AcademicClassViewSet(ModelViewSet):
    """
    API endpoint for managing Academic Classes.
    Only accessible to authenticated school admins.
    """
    serializer_class = AcademicClassSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get_queryset(self):
        # Ensure only classes belonging to the user's school are returned
        user = self.request.user
        return AcademicClass.objects.filter(school=user.school)


class SubjectViewSet(ModelViewSet):
    """
    API endpoint for managing Subjects.
    Only accessible to authenticated school admins.
    """
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsSchoolAdmin]

    def get_queryset(self):
        # Ensure only subjects belonging to the user's school are returned
        user = self.request.user
        return Subject.objects.filter(school=user.school)

