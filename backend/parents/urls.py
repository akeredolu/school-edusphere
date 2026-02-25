from django.urls import path
from .views import ParentDashboardView

urlpatterns = [
    path("parent/dashboard/", ParentDashboardView.as_view(), name="parent-dashboard"),

]

