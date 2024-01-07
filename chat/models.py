from django.db import models
from accounts.models import CustomUser
from task_board.models import Board
# Create your models here.


class Message(models.Model):

  board = models.ForeignKey(Board, on_delete=models.CASCADE)
  sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  message_type = models.CharField(blank=True, null=True, default='text')
  content = models.TextField()

  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
      return f"{self.sender.username} - {self.created_at}"