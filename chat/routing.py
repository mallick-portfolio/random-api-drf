from django.urls import path

from .import consumers

ws_patterns = [
  path("ws/message/<str:room_name>/", consumers.MessageConsumer.as_asgi()),
]