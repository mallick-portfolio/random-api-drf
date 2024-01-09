from notification.models import Notification
from notification.serializers import NotificationSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def create_notification(user, receiver, message):
  channel_layer = get_channel_layer()
  notification = Notification.objects.create(sender=user, receiver=receiver, message=message)
  data = NotificationSerializer(notification).data
  async_to_sync(channel_layer.group_send)(
      f'notification_{receiver.id}',
      {
          'type': 'send_notification',
          'message': data
      }
  )
