import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import CustomUser
from notification.models import Notification
from notification.serializers import NotificationSerializer

class NotificationConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['receiver_id']
    self.room_group_name = f'notification_{self.room_name}'
    print(self.room_group_name)
    await self.channel_layer.group_add(self.room_group_name, self.channel_name)
    await self.accept()


  # receive notification
  async def receive(self, text_data=None, bytes_data=None):
    sender = await self.get_user(self.scope['user'])
    receiver = await self.get_user(self.room_name)
    text_data_json = json.loads(text_data)

    await self.channel_layer.group_send(
            self.room_group_name, {"type": "send_notification", "message": text_data_json}
        )

  async def send_notification(self, event):
    message = event["message"]
    await self.send(text_data=json.dumps({"message": message}))

  # disconnect notification
  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


  @database_sync_to_async
  def get_user(self, id):
    user = CustomUser.objects.filter(id=id).first()
    return user



