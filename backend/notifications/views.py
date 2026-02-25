from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_notifications(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by("-created_at")

    return Response(NotificationSerializer(notifications, many=True).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mark_as_read(request, pk):
    notification = Notification.objects.get(
        pk=pk, recipient=request.user
    )
    notification.is_read = True
    notification.save()
    return Response({"status": "read"})
