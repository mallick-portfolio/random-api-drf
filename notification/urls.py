from django.urls import path
from notification import views

urlpatterns = [
    path('', views.NotificationAPIView.as_view(), name='NotificationView'),
    path('<int:pk>/', views.NotificationAPIView.as_view(), name='NotificationDetails'),
]
