from rest_framework import serializers
from chat.models import Message, MessageAttachments
from accounts.serializers import UserSerializer

class MessageAttachmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = MessageAttachments
    fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
  message_attachments = MessageAttachmentSerializer(many=True, read_only=True)
  sender = UserSerializer()
  class Meta:
    model = Message
    fields = "__all__"
