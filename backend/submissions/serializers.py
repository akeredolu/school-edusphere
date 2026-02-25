from rest_framework import serializers
from .models import Submission

class SubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.get_full_name",
        read_only=True
    )

    class Meta:
        model = Submission
        fields = "__all__"

