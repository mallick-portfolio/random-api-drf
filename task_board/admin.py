from django.contrib import admin
from task_board.models import Board, TaskItem, Task, BoardInvitation, TaskLabel, TaskComment, TaskAttachments
# Register your models here.
admin.site.register(Board)
admin.site.register(TaskItem)
admin.site.register(Task)
admin.site.register(BoardInvitation)
admin.site.register(TaskLabel)
admin.site.register(TaskComment)
admin.site.register(TaskAttachments)