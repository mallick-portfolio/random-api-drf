from django.db import models
from accounts.models import CustomUser
from task_board.models import Board
# Create your models here.


class Message(models.Model):

  board = models.ForeignKey(Board, on_delete=models.CASCADE)
  sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  content = models.TextField(blank=True, null=True)
  message_type = models.CharField(max_length=20, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)


class MessageAttachments(models.Model):
  MEDIA_TYPE = (
    ('file', 'file'),
    ('image', 'image'),
  )
  message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='attachments')
  image = models.ImageField(upload_to="message/media", blank=True, null=True)
  media_file = models.FileField(upload_to="message/media", blank=True, null=True)
  media_type = models.CharField(max_length=10, choices=MEDIA_TYPE, blank=True, null=True)