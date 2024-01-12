from django.urls import path
from .views import *
urlpatterns = [
    path('attachments/', MessageAttachmentsView.as_view(), name='MessageAttachment'),
]
