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


class MessageAttachments(models.Model):
  message = models.ForeignKey(Message, on_delete=models.CASCADE, blank=True, null=True, related_name='message_attachments')
  image = models.ImageField(upload_to="message/media", blank=True, null=True)
  file = models.FileField(upload_to="message/media", blank=True, null=True)