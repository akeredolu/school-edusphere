from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.permissions import IsTeacher, IsStudent
from .models import Exam, StudentExam
from .serializers import ExamSerializer
from .services import grade_exam
from django.utils.timezone import now

class ExamViewSet(ModelViewSet):
    serializer_class = ExamSerializer
    permission_classes = [IsTeacher]

    def get_queryset(self):
        return Exam.objects.filter(school=self.request.user.school)


class SubmitExamView(APIView):
    permission_classes = [IsStudent]

    def post(self, request, exam_id):
        student_exam = StudentExam.objects.get(
            exam_id=exam_id,
            student=request.user.studentprofile
        )
        student_exam.submitted_at = now()
        grade_exam(student_exam)

        return Response({
            "score": student_exam.score,
            "message": "Exam submitted successfully"
        })

