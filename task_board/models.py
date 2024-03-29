from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Board(models.Model):
  unique_id = models.CharField(max_length=255, blank=True, null=True, unique=True)
  title = models.CharField(max_length=100)
  description = models.TextField(blank=True, null=True)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, )
  authorize_users = ArrayField(models.CharField(max_length=20, null=True, blank=True), null=True, blank=True)
  status = models.BooleanField(default=False)

  # time stapm
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=False,null=True, blank=True)


class TaskItem(models.Model):
  title = models.CharField(max_length=150)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
  board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True, related_name='task_items')
  position = models.PositiveIntegerField(blank=True, null=True)

  # time stapm
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=False, blank=True, null=True)


class Task(models.Model):
  title = models.CharField(max_length=150)
  description = models.TextField(blank=True, null=True)
  banner = models.ImageField(upload_to='taskboard/', max_length=None, null=True, blank=True)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
  task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
  position = models.PositiveIntegerField(blank=True, null=True)
  status = models.BooleanField(default=False)
  authorize_users = ArrayField(models.CharField(max_length=20, null=True, blank=True), null=True, blank=True)

  # time stapm
  created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=False, blank=True, null=True)


class BoardInvitation(models.Model):
  board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='boards')
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  status = models.CharField(default='pending', max_length=20)
  created_at = models.DateTimeField(auto_now_add=True)

class TaskLabel(models.Model):
  task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='taskLabels')
  title = models.CharField(max_length=20)
  is_completed = models.BooleanField(default=False)


class TaskComment(models.Model):
  task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_comments', blank=True, null=True)
  content = models.TextField()
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
  comment_type = models.CharField(max_length=20, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

class TaskAttachments(models.Model):
  MEDIA_TYPE = (
    ('file', 'file'),
    ('image', 'image'),
  )
  comment = models.ForeignKey(TaskComment, on_delete=models.CASCADE, related_name='task_attachments')
  image = models.ImageField(upload_to="comment/", blank=True, null=True)
  media_file = models.FileField(upload_to="comment/", blank=True, null=True)
  media_type = models.CharField(max_length=10, choices=MEDIA_TYPE, blank=True, null=True)

