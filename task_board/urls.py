from django.urls import path
from task_board import views

urlpatterns = [
    path('', views.BoardAPIView.as_view(), name='BoardAPI'),
    path('<int:pk>/', views.BoardAPIView.as_view(), name='board-details'),
    path('task-item/', views.TaskItemAPI.as_view(), name='TaskItemAPI'),
    path('task/', views.TaskAPI.as_view(), name='TaskAPI')
]
