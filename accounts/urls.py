
from django.urls import path
from accounts import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('register/', views.RegistrationAPIView.as_view(), name='register' ),
    path('login/', views.LoginAPIView.as_view(), name='login' ),
    path('logout/', views.LogoutAPIView.as_view(), name='logout' ),
    path('verify-email-otp/', views.VerifyEmailOTP.as_view(), name='logout' ),
    path('me/', views.MeAPI.as_view(), name='me' ),
    path('update-password/', views.UpdatePassword.as_view(), name='UpdatePassword' ),
    path("users/", views.users, name="users"),
    path('token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]
