from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from accounts.models import CustomUser
from task_board.models import Board
from chat.models import Message
from chat.serializers import MessageSerializer

from asgiref.sync import sync_to_async
from logging import getLogger
from functools import wraps
from inspect import iscoroutinefunction
from channels.exceptions import AcceptConnection, DenyConnection, StopConsumer


logger = getLogger()



class MessageConsumer(AsyncWebsocketConsumer):

  # connect connection and accept new connectiong
  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = f'board_{self.room_name}'
    self.user = self.scope['user']
    if self.user is None:
      await self.close()

    await self.channel_layer.group_add(self.room_group_name, self.channel_name)
    await self.accept()

  async def receive(self, text_data=None, bytes_data=None):
    print(json.loads(text_data))
    user =await self.get_user_data()
    board =await self.get_board_data()
    text_data_json = json.loads(text_data)
    content = text_data_json.get('content')
    message_type = text_data_json['message_type']

    new_msg =await self.create_chat(content,message_type, user, board)


    await self.channel_layer.group_send(self.room_group_name, {
        'type': 'chat_message',
        'message': new_msg,
    })


  # disconnect
  async def disconnect(self, code):
    await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


  async def chat_message(self, event):
    message = event['message']
    await self.send(text_data=json.dumps(message))


  # get user details
  @database_sync_to_async
  def get_user_data(self):
    user = CustomUser.objects.filter(id=self.scope['user']).first()
    return user

  # get board details
  @database_sync_to_async
  def get_board_data(self):
    board = Board.objects.filter(unique_id=self.room_name).first()
    return board

  @database_sync_to_async
  def create_chat(self, content,message_type, user, board):
    msg = Message.objects.create(board=board,sender=user, content=content,message_type=message_type)
    data = MessageSerializer(msg).data
    return data