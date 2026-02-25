"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import communications.routing
import virtual_classroom.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Standard Django ASGI application for HTTP requests
django_asgi_app = get_asgi_application()

# ASGI application with Channels support (HTTP + WebSocket)
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            communications.routing.websocket_urlpatterns
            + virtual_classroom.routing.websocket_urlpatterns
        )
    ),
})

