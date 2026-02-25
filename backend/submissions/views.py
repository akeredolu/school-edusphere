from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.utils.timezone import now
from .models import Submission
from .serializers import SubmissionSerializer

class SubmissionViewSet(ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "student":
            return Submission.objects.filter(student=user)

        if user.role == "teacher":
            return Submission.objects.filter(
                assignment__created_by=user
            )

        return Submission.objects.none()

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    def perform_update(self, serializer):
        serializer.save(graded_at=now())
