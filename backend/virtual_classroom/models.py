from django.db import models
from django.conf import settings
from academics.models import AcademicClass, Subject
import uuid
from django.utils import timezone


class VirtualClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    academic_class = models.ForeignKey(AcademicClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'}
    )
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    # Paste the Jitsi meeting link here, e.g., https://meet.jit.si/school-class-physics-ss2
    meeting_link = models.URLField(blank=True, null=True, help_text="Jitsi meeting link for the class")
    
    is_live = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class VirtualAttendance(models.Model):
    virtual_class = models.ForeignKey(
        VirtualClass,
        on_delete=models.CASCADE,
        related_name='attendances'
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='virtual_attendances'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(blank=True, null=True)
    duration_seconds = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.student.email} - {self.virtual_class.title}"


class ClassJoinToken(models.Model):
    virtual_class = models.ForeignKey(VirtualClass, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.used and timezone.now() < self.expires_at

    def __str__(self):
        return f"Token for {self.user.email} - {self.virtual_class.title}"

class ClassRecording(models.Model):
    virtual_class = models.ForeignKey(
        VirtualClass,
        on_delete=models.CASCADE,
        related_name="recordings"
    )
    title = models.CharField(max_length=255)
    video_url = models.URLField()
    duration_seconds = models.PositiveIntegerField()
    recorded_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.virtual_class.title} recording"


class ClassChatMessage(models.Model):
    virtual_class = models.ForeignKey(
        VirtualClass,
        on_delete=models.CASCADE,
        related_name="chat_messages"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    message = models.TextField()
    is_announcement = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} - {self.message[:30]}"

class ClassReaction(models.Model):
    REACTIONS = (
        ("like", "👍"),
        ("clap", "👏"),
        ("question", "❓"),
    )

    virtual_class = models.ForeignKey(VirtualClass, on_delete=models.CASCADE)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "student"}
    )
    reaction = models.CharField(max_length=20, choices=REACTIONS)
    created_at = models.DateTimeField(auto_now_add=True)
