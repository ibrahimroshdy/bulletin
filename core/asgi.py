"""
ASGI config for bulletin project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()
# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.

from apps.system.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
        {
            "http":
                get_asgi_application(),
            "websocket":
                AuthMiddlewareStack(URLRouter(websocket_urlpatterns))

        }
)
