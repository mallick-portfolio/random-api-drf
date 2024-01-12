from rest_framework import serializers
from chat.models import Message, MessageAttachments
from accounts.serializers import UserSerializer

class MessageAttachmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageAttachments
        fields ="__all__"

class MessageSerializer(serializers.ModelSerializer):
  sender = UserSerializer()
  attachments = MessageAttachmentsSerializer(many=True, read_only=True)
  class Meta:
    model = Message
    fields = "__all__"
