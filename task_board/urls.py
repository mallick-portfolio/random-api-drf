from django.urls import path
from task_board import views

urlpatterns = [
    path('', views.BoardAPIView.as_view(), name='board-create'),
    path('<int:pk>/', views.BoardAPIView.as_view(), name='board-details'),
]
