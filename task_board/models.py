from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Board(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField(blank=True, null=True)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, )
  authorize_users = ArrayField(models.CharField(max_length=20, null=True, blank=True), null=True, blank=True)

  # time stapm
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=False,null=True, blank=True)


class TaskItem(models.Model):
  title = models.CharField(max_length=150)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
  board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True)
  position = models.PositiveIntegerField(blank=True, null=True)

  # time stapm
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=False, blank=True, null=True)


class Task(models.Model):
  title = models.CharField(max_length=150)
  banner = models.ImageField(upload_to='taskboard/', max_length=None, null=True, blank=True)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
  task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE, null=True, blank=True)
  position = models.PositiveIntegerField(blank=True, null=True)
  # time stapm
  created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=False, blank=True, null=True)



