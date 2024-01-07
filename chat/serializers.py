from rest_framework import serializers
from chat.models import Message
from accounts.models import CustomUser

class MessageSerializer(serializers.ModelSerializer):
  user = serializers.SerializerMethodField('get_user')
  class Meta:
    model = Message
    fields = "__all__"
    read_only_fields = ['user']

  @staticmethod
  def get_user(obj):
    user = CustomUser.objects.filter(id=obj.user.id).values('id', 'first_name', 'last_name').first()
    return user
