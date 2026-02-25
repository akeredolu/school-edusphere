from django.urls import path
from .views import my_notifications, mark_as_read

urlpatterns = [
    path("", my_notifications),
    path("<int:pk>/read/", mark_as_read),
]

