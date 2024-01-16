from rest_framework import serializers
from task_board.models import Board, TaskItem, Task, BoardInvitation, TaskLabel, TaskComment, TaskAttachments
from accounts.models import CustomUser
from accounts.serializers import UserSerializer



class BoardSerializer(serializers.ModelSerializer):

  user = serializers.SerializerMethodField('get_user')
  authorize_users = serializers.SerializerMethodField('get_authorize_users')
  class Meta:
    model = Board
    fields = "__all__"
    read_only_fields = ['user', 'authorize_users']

  @staticmethod
  def get_user(obj):
    user = CustomUser.objects.filter(id=obj.user.id).values('id', 'first_name', 'last_name').first()
    return user


  @staticmethod
  def get_authorize_users(obj):
    members = []
    for id in obj.authorize_users:
      data = CustomUser.objects.filter(id=id).values('id', 'first_name', 'last_name', 'email').first()
      members.append(data)
    return members


class BoardUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Board
    fields = ['title', 'description', 'authorize_users']

  def update(self, instance, validated_data):
    instance.title = validated_data.get('title',instance.title)
    instance.description = validated_data.get('description',instance.description)
    instance.authorize_users = validated_data.get('authorize_users',instance.authorize_users)
    instance.save()
    return instance



class TaskAttachmentsSerializer(serializers.ModelSerializer):
  class Meta:
    model = TaskAttachments
    fields = "__all__"


class TaskCommentSerializer(serializers.ModelSerializer):
  task_attachments = TaskAttachmentsSerializer(many=True, read_only=True)
  user = serializers.SerializerMethodField('get_user')
  class Meta:
    model = TaskComment
    fields = "__all__"
    read_only_fields = ['user',]

  @staticmethod
  def get_user(obj):
    user = CustomUser.objects.get(id=obj.user.id)
    data = UserSerializer(user).data
    return data




class TaskItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = TaskItem
    fields = '__all__'

class TaskLabelSerializer(serializers.ModelSerializer):
  class Meta:
    model = TaskLabel
    fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
  taskLabels = TaskLabelSerializer(many=True, read_only=True)
  task_comments = TaskCommentSerializer(many=True, read_only=True)
  class Meta:
    model = Task
    fields = '__all__'





class BoardInvitationSerializer(serializers.ModelSerializer):
  class Meta:
    model = BoardInvitation
    fields = '__all__'
