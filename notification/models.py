from django.db import models
from accounts.models import CustomUser
# Create your models here.
class Notification(models.Model):
  sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='senders')
  receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='receivers', blank=True, null=True)
  message = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
