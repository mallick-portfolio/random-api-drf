from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from accounts.models import CustomUser
import jwt
import os

class ChatConsumer(WebsocketConsumer):
  def connect(self):
    self.room_name = 'test'
    self.room_group_name = 'test-group'

    async_to_sync(self.channel_layer.group_add)(
     self.room_group_name, self.channel_name
    )
    self.accept()
    self.send(text_data=json.dumps({
      "message": "connected yeah i can fuck"
    }))

  def receive(self, text_data=None, bytes_data=None):
    print(text_data)
    self.send(text_data=json.dumps({
      "data": text_data
    }))
    return super().receive(text_data, bytes_data)

  def disconnect(self, code):
    print(code, "disconnected")
    return super().disconnect(code)


class NewConsumer(AsyncWebsocketConsumer):
  # def
  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = f'chat_{self.room_name}'
    await self.channel_layer.group_add(self.room_group_name, self.channel_name)
    await self.accept()
    await self.send(text_data=json.dumps({
      "message": "Websocket connected"
    }))

  async def receive(self, text_data=None):
    message = json.loads(text_data)
    message['type'] = 'text'
    await self.channel_layer.group_send(
          self.room_group_name, {"type": "chat_message", "message": message}
        )
    # return await super().receive(text_data, bytes_data)

  async def disconnect(self, code):
    print('socket disconnected')
    await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

  async def chat_message(self, event):
    print(event)
    await  self.send(text_data=json.dumps(event))



class MessageConsumer(AsyncWebsocketConsumer):

  # connect connection and accept new connectiong
  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = f'board_{self.room_name}'
    self.user = self.scope['user']
    print(self.user)
    if self.user is None:
      await self.close()

    await self.channel_layer.group_add(self.room_group_name, self.channel_name)
    await self.accept()

  async def receive(self, text_data=None, bytes_data=None):

    # user = await self.get_user_data()
    message = json.loads(text_data)
    print(message)


  # disconnect
  async def disconnect(self, code):
    await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


  @database_sync_to_async
  def get_user_data(self):
    user = CustomUser.objects.filter(id=self.scope['user']).first()
    return user
