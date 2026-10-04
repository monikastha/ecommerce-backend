from channels.generic.websocket import AsyncWebsocketConsumer
import json


class AssistantNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'assistant_notifications'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        # Clients shouldn't need to send messages for now.
        pass

    async def notification_message(self, event):
        # event['message'] expected to be JSON-serializable
        await self.send(text_data=json.dumps(event.get('message', {})))
