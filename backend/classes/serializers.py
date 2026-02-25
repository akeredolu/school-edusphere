from rest_framework import serializers
from .models import Class, ClassSession
from .models import Enrollment

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = "__all__"
        read_only_fields = ["teacher"]


class ClassSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSession
        fields = "__all__"


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source="student.get_full_name",
        read_only=True
    )

    class Meta:
        model = Enrollment
        fields = "__all__"
