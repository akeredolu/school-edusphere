from rest_framework import serializers
from .models import VirtualClass

class VirtualClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualClass
        fields = "__all__"
        read_only_fields = ["teacher", "is_live"]

