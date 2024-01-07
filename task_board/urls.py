from django.urls import path
from task_board import views

urlpatterns = [
    path('', views.BoardAPIView.as_view(), name='BoardAPI'),

    path('task-item/', views.TaskItemAPI.as_view(), name='TaskItemAPI'),
    path('task/<int:pk>/', views.TaskAPI.as_view(), name='TaskDetailAPI'),
    path('task-item/<int:pk>/', views.TaskItemAPI.as_view(), name='TaskItemDetailsAPI'),
    path('task/', views.TaskAPI.as_view(), name='TaskAPI'),
    path('<str:unique_id>/', views.BoardAPIView.as_view(), name='BoardDetailAPI'),
    path('invite-board-member/<str:unique_id>', views.BoardMember.as_view(), name='BoardMember'),

]
