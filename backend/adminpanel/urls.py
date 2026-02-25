from django.urls import path
from .views import admin_overview, admin_users

urlpatterns = [
    path("overview/", admin_overview),
    path("users/", admin_users),
]

