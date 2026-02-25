from django.urls import re_path
from .consumers import ClassPresenceConsumer, ClassChatConsumer

websocket_urlpatterns = [
    # Presence / attendance
    re_path(
        r"ws/class/(?P<class_id>[^/]+)/$",
        ClassPresenceConsumer.as_asgi(),
    ),

    # Class chat
    re_path(
        r"ws/class/(?P<class_id>[^/]+)/chat/$",
        ClassChatConsumer.as_asgi(),
    ),
]

