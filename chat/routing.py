from django.urls import path, re_path

from .import consumers
from notification.consumers import NotificationConsumer

ws_patterns = [
  path("ws/message/<str:room_name>/", consumers.MessageConsumer.as_asgi()),
  re_path((r'ws/notification/(?P<receiver_id>\w+)/$'), NotificationConsumer.as_asgi()),
]