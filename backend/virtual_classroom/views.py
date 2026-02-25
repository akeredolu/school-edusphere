from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import VirtualClass
from .serializers import VirtualClassSerializer
from .permissions import IsTeacher
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import VirtualClass, VirtualAttendance, ClassJoinToken
from .models import VirtualAttendance
from .models import ClassRecording, VirtualClass


class VirtualClassViewSet(ModelViewSet):
    serializer_class = VirtualClassSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "teacher":
            return VirtualClass.objects.filter(teacher=user)
        return VirtualClass.objects.filter(academic_class__students=user)

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user)


class JoinVirtualClassView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, class_id):
        token_value = request.data.get("token")

        token = ClassJoinToken.objects.get(
            token=token_value,
            virtual_class_id=class_id,
            user=request.user
        )

        if not token.is_valid():
            return Response({"detail": "Invalid or expired token"}, status=403)

        token.used = True
        token.save()

        VirtualAttendance.objects.create(
            virtual_class=token.virtual_class,
            student=request.user
        )

        return Response({
            "meeting_link": token.virtual_class.meeting_link
        })
        

class StartVirtualClassView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, class_id):
        virtual_class = VirtualClass.objects.get(id=class_id, teacher=request.user)
        virtual_class.is_live = True
        virtual_class.save()

        return Response({"status": "Class started"})

class LiveAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, class_id):
        attendance = VirtualAttendance.objects.filter(
            virtual_class_id=class_id
        )

        return Response([
            {
                "student": a.student.get_full_name(),
                "joined_at": a.joined_at,
                "left_at": a.left_at,
                "duration": a.duration_seconds
            } for a in attendance
        ])
        

class AddRecordingView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, class_id):
        virtual_class = VirtualClass.objects.get(
            id=class_id,
            teacher=request.user
        )

        recording = ClassRecording.objects.create(
            virtual_class=virtual_class,
            title=request.data["title"],
            video_url=request.data["video_url"],
            duration_seconds=request.data["duration"]
        )

        virtual_class.is_live = False
        virtual_class.save()

        return Response({"status": "recording added"})


class ClassRecordingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, class_id):
        recordings = ClassRecording.objects.filter(
            virtual_class_id=class_id
        )

        return Response([
            {
                "title": r.title,
                "video_url": r.video_url,
                "duration": r.duration_seconds,
                "recorded_at": r.recorded_at
            }
            for r in recordings
        ])
