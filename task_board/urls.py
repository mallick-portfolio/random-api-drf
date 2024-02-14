from django.urls import path, include
from task_board import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', views.TaskLabelViewSet)


urlpatterns = [
    path('task-label/',  include(router.urls)),
    path('', views.BoardAPIView.as_view(), name='BoardAPI'),
    path('public/', views.PublicBoardAPIView.as_view(), name='PublicBoardAPIView'),
    path('public/<str:unique_id>/', views.PublicBoardAPIView.as_view(), name='PublicBoardAPIView'),
    path('task-item/', views.TaskItemAPI.as_view(), name='TaskItemAPI'),
    path('task-item/<int:pk>/', views.TaskItemAPI.as_view(), name='TaskItemDetailsAPI'),
    path('task/', views.TaskAPI.as_view(), name='TaskAPI'),
    path("task/task-comment/attachment/", views.CommentAttachmentsView.as_view(), name="commentattachment"),
    path("task/assign-member/<int:task_id>/", views.AssignTaskMember.as_view(), name="assignmember"),
    path("task/task-comment/", views.TaskCommentAPI.as_view(), name="taskcomment"),
    path('public-task/<int:pk>/', views.PublicTaskAPI.as_view(), name='PublicTaskAPI'),
    path('task/<int:pk>/', views.TaskAPI.as_view(), name='TaskDetailAPI'),
    path('<str:unique_id>/', views.BoardAPIView.as_view(), name='BoardDetailAPI'),
    path('invite-board-member/<str:action_type>/', views.BoardMember.as_view(), name='BoardMember'),

]
