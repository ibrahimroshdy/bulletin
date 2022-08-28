# chat/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/machine_uptime/$", consumers.UptimeConsumer.as_asgi()),
]
