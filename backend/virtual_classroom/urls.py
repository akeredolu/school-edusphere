from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VirtualClassViewSet,
    JoinVirtualClassView,
    StartVirtualClassView,
    AddRecordingView,
)

router = DefaultRouter()
router.register("classes", VirtualClassViewSet, basename="virtual-classes")

urlpatterns = [
    path("", include(router.urls)),
    path("classes/<uuid:class_id>/join/", JoinVirtualClassView.as_view()),
    path("classes/<uuid:class_id>/start/", StartVirtualClassView.as_view()),
    path(
        "classes/<uuid:class_id>/recordings/",
        AddRecordingView.as_view(),
    ),
]

