from django.db import models
from accounts.models import CustomUser
from task_board.models import Board
# Create your models here.


class Message(models.Model):
  MESSAGE_TYPE = (
     ('text', 'text'),
     ('media', 'media'),
  )
  board = models.ForeignKey(Board, on_delete=models.CASCADE)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  message_type = models.CharField(choices=MESSAGE_TYPE,blank=True, null=True)
  content = models.TextField()

  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f"{self.user.username} - {self.created_at}"