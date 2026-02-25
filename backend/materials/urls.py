from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import LearningMaterialViewSet, AssignmentViewSet, AssignmentSubmissionViewSet, MaterialViewSet

router = DefaultRouter()
router.register(r'materials', LearningMaterialViewSet, basename='material')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'submissions', AssignmentSubmissionViewSet, basename='submission')

urlpatterns = [
    path('', include(router.urls)),
]

