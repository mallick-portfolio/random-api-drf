from django.urls import path
from task_board import views

urlpatterns = [
    path('create/', views.BoardAPIView.as_view(), name='board-create'),
]
