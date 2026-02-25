# schools/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet

router = DefaultRouter()
router.register('', SchoolViewSet, basename='school')  # root path of this app

urlpatterns = [
    path('', include(router.urls)),  # include all router-generated endpoints
]

