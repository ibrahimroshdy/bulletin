# chat/routing.py
from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/machine_uptime/(?P<user_id>\w+)/$', consumers.UptimeConsumer.as_asgi()),
    # re_path(r'^ws/datetime/(?P<user_id>\w+)/$', consumers.DatetimeConsumer.as_asgi()),
]
