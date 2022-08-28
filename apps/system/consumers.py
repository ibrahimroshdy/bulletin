# system/consumers.py
import json
import datetime
from uptime import uptime
import os
from channels.generic.websocket import WebsocketConsumer
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import time
from . import utils
from asgiref.sync import async_to_sync,sync_to_async


class UptimeConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        while True:
            self.send(text_data=json.dumps({
                'message': utils.machine_uptime_func()
            }))
            time.sleep(3)
            # Send message to WebSocket


    def disconnect(self, close_code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        pass

    # def machine_uptime_message(self):
