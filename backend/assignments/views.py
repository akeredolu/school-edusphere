from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Assignment
from .serializers import AssignmentSerializer

class AssignmentViewSet(ModelViewSet):
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "teacher":
            return Assignment.objects.filter(created_by=user)

        if user.role == "student":
            return Assignment.objects.filter(
                classroom__enrollments__student=user
            )

        return Assignment.objects.none()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
