from rest_framework.viewsets import ModelViewSet
from .models import School
from .serializers import SchoolSerializer
from accounts.permissions import IsSchoolAdmin

class SchoolViewSet(ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsSchoolAdmin]
