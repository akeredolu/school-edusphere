from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from accounts.permissions import IsTeacher, IsStudent
from .models import LearningMaterial, Assignment, AssignmentSubmission
from .serializers import (
    LearningMaterialSerializer,
    AssignmentSerializer,
    AssignmentSubmissionSerializer
)
from .models import Material
from .serializers import MaterialSerializer



class LearningMaterialViewSet(ModelViewSet):
    serializer_class = LearningMaterialSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return LearningMaterial.objects.filter(
            school=self.request.user.school
        )


class AssignmentViewSet(ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return Assignment.objects.filter(
            school=self.request.user.school
        )


class AssignmentSubmissionViewSet(ModelViewSet):
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return AssignmentSubmission.objects.filter(
            student=self.request.user.studentprofile
        )

class MaterialViewSet(ModelViewSet):
    queryset = Material.objects.all() 
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "teacher":
            return Material.objects.filter(created_by=user)

        if user.role == "student":
            return Material.objects.filter(
                classroom__enrollments__student=user,
                is_active=True
            )

        return Material.objects.none()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
