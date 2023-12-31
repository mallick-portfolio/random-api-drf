from rest_framework import serializers
from task_board.models import Board, TaskItem, Task
from accounts.models import CustomUser

class BoardSerializer(serializers.ModelSerializer):
  user = serializers.SerializerMethodField('get_user')
  authorize_users = serializers.SerializerMethodField('get_members')
  class Meta:
    model = Board
    fields = "__all__"

  @staticmethod
  def get_user(obj):
    user = CustomUser.objects.filter(id=obj.user.id).values('id', 'first_name', 'last_name').first()
    return user


  @staticmethod
  def get_members(obj):
    members = []
    print(obj.authorize_users)
    for id in obj.authorize_users:
      data = CustomUser.objects.filter(id=id).values('id', 'first_name', 'last_name', 'email').first()
      members.append(data)
    return members




class TaskItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = TaskItem
    fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = '__all__'
