# system/consumers.py
import asyncio
import datetime
import json
import os

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from . import utils


class UptimeConsumer(AsyncWebsocketConsumer):
    """
    Uptime Consumer
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_id = None
        self.room_group_name = None
        self.is_connected = None

    async def connect(self):
        """
        Websocket connection
        :return:
        """
        # if self.scope['user'] == AnonymousUser():
        #     await self.close()
        #     return

        self.user_id = self.scope['user'].id
        self.room_group_name = f'BULLETIN_UPTIME_GROUP_NAME_{self.user_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        self.is_connected = True
        while self.is_connected:
            await asyncio.sleep(1)

            await self.send(text_data=json.dumps({
                'message': utils.machine_uptime_func()
            }))

    async def disconnect(self, code):

        # set is_connected to false
        self.is_connected = False
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


class DatetimeConsumer(AsyncWebsocketConsumer):
    """
    Datetime Consumer
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user_id = None
        self.room_group_name = None
        self.is_connected = None

    async def connect(self):
        """
        Websocket connection
        :return:
        """
        # if self.scope['user'] == AnonymousUser():
        #     await self.close()
        #     return

        self.user_id = self.scope['user'].id
        self.room_group_name = f'BULLETIN_DATETIME_GROUP_NAME_{self.user_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        self.is_connected = True
        while self.is_connected:
            await asyncio.sleep(1)

            await self.send(text_data=json.dumps({
                'message': datetime.datetime.now()
            }, indent=4, sort_keys=True, default=str))

    async def disconnect(self, code):

        # set is_connected to false
        self.is_connected = False
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
