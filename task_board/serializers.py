from rest_framework import serializers
from task_board.models import Board, TaskItem, Task

class BoardSerializer(serializers.ModelSerializer):
  class Meta:
    model = Board
    fields = '__all__'

class TaskItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = TaskItem
    fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
  class Meta:
    model = Task
    fields = '__all__'
