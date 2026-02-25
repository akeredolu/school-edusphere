from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import TeacherClassViewSet, ClassSessionViewSet, EnrollmentViewSet, StudentClassesView

router = DefaultRouter()
router.register("classes", TeacherClassViewSet, basename="classes")
router.register("sessions", ClassSessionViewSet, basename="sessions")

router.register("enrollments", EnrollmentViewSet, basename="enrollments")


urlpatterns = router.urls + [
    path("student/classes/", StudentClassesView.as_view()),
]




