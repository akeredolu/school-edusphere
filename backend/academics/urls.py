from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AcademicClassViewSet, SubjectViewSet

router = DefaultRouter()
router.register(r'classes', AcademicClassViewSet, basename='academicclass')
router.register(r'subjects', SubjectViewSet, basename='subject')

urlpatterns = [
    path('', include(router.urls)),
]

