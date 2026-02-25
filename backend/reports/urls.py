from django.urls import path
from .views import (
    attendance_report,
    assignment_report,
    performance_report
)

urlpatterns = [
    path("attendance/", attendance_report),
    path("assignments/", assignment_report),
    path("performance/", performance_report),
]

