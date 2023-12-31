
from django.urls import path
from accounts import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view(), name='register' ),
    path('login/', views.LoginAPIView.as_view(), name='login' ),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]
