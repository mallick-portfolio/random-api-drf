from django.urls import path
from .views import *
urlpatterns = [
    path('<int:message_id>/', MessageAttachmentUploadView.as_view(), name='MessageAttachment'),
]
