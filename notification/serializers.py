from rest_framework import serializers
from notification.models import Notification
from accounts.serializers import UserSerializer
class NotificationSerializer(serializers.ModelSerializer):
  sender = UserSerializer()
  class Meta:
    model = Notification
    fields = '__all__'
