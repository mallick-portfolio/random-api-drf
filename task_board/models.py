from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
# Create your models here.
class Board(models.Model):
  title = models.CharField(_("board name"), max_length=100)
  description = models.TextField(_("board description"))
  creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, )
  authorize_users = models.ManyToManyField(CustomUser, related_name='boards')

  # time stapm
  created_at = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=False, auto_now_add=False,null=True, blank=True)


class TaskItem(models.Model):
  title = models.CharField(_("task item title"), max_length=150)
  creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
  board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, blank=True)

  # time stapm
  created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)


class Task(models.Model):
  title = models.CharField(_("task title"), max_length=150)
  banner = models.ImageField(_("task banner image"), upload_to='taskboard/', max_length=None)
  creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
  task_item = models.ForeignKey(TaskItem, on_delete=models.CASCADE, null=True, blank=True)
   # time stapm
  created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=False, auto_now_add=False)



