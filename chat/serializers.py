from rest_framework import serializers
from chat.models import Message
from accounts.serializers import UserSerializer
class MessageSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  class Meta:
    model = Message
    fields = "__all__"
