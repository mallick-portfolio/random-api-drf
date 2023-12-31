from django.contrib import admin
from task_board.models import Board, TaskItem, Task
# Register your models here.
admin.site.register(Board)
admin.site.register(TaskItem)
admin.site.register(Task)