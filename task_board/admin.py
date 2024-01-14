from django.contrib import admin
from task_board.models import Board, TaskItem, Task, BoardInvitation, TaskLabel
# Register your models here.
admin.site.register(Board)
admin.site.register(TaskItem)
admin.site.register(Task)
admin.site.register(BoardInvitation)
admin.site.register(TaskLabel)