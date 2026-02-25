from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Class, ClassSession
from .serializers import ClassSerializer, ClassSessionSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Class, Enrollment
from .serializers import EnrollmentSerializer
from rest_framework.views import APIView


class TeacherClassViewSet(ModelViewSet):
    serializer_class = ClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Class.objects.filter(teacher=self.request.user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class ClassSessionViewSet(ModelViewSet):
    serializer_class = ClassSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ClassSession.objects.filter(
            classroom__teacher=self.request.user
        )


class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "teacher":
            return Enrollment.objects.filter(
                classroom__teacher=user
            )

        if user.role == "student":
            return Enrollment.objects.filter(student=user)

        return Enrollment.objects.none()

    def perform_create(self, serializer):
        serializer.save()



class StudentClassesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        enrollments = Enrollment.objects.filter(student=request.user)
        classes = [e.classroom for e in enrollments]

        return Response(
            ClassSerializer(classes, many=True).data
        )
