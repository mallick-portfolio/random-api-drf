from django.shortcuts import render
from .serializers import RegistrationSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from . import helpers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import random

from accounts.models import CustomUser
# Create your views here.
import traceback

class RegistrationAPIView(APIView):
  def post(self, request):


    try:
      data = request.data
      otp = helpers.generate_otp(6)
      data['otp'] = int(otp)
      serializer = RegistrationSerializer(data=data)
      if serializer.is_valid():
        email = request.data['email']
        serializer.save()
        # helpers.send_otp_email(email,data,'Verify OTP Code', './email/verifyEmail.html')
        return Response({
          "success": True,
          "status": status.HTTP_201_CREATED,
          'message': "Registration successfull!!!. Please check your email."
        })
      else:
        return Response({
          "success": False,
          "status": status.HTTP_400_BAD_REQUEST,
          'message': "Registration failed.Username or email already exist",
          'error': True
        })
    except Exception as e:
      return Response({'message':'fail','error':e,"status": status.HTTP_500_INTERNAL_SERVER_ERROR})


class VerifyEmailOTP(APIView):
  def post(self, request):
    try:

      data = request.data
      user = CustomUser.objects.filter(email=data['email'],otp=data['otp']).first()
      print(user)
      if user is not None:
        otp_expire = helpers.compare_minute(user.otp_created_at)
        if not otp_expire:
          user.is_email_verified = True
          user.otp = None
          user.save()
          return Response({
            "success": True,
            'message': "Your email verify successfully!!!",
            "data": None
          })
        else:
          return Response({
              "success": False,
              'message': "Your otp time expire. Please try again!!!",
            })
      else:
        return Response({
            "success": False,
            'message': "Invalid otp",
          })
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })





class LoginAPIView(APIView):
  def post(self, request):
    print(request.data)
    try:
      rd = request.data
      if 'email' not in rd or 'password' not in rd:
        return Response({
          "success": False,
          'message': "Invalid Credentials",
        })
      email = rd['email']
      password = rd['password']
      user = authenticate(request, email=email, password=password)
      if user is not None:
        login(request, user=user)
        token = helpers.get_tokens_for_user(user)
        return Response({
          "success": True,
          'message': "Login successfull!!!",
          "token": token
        })
      else:
        return Response({
          "success": False,
          'message': "Invalid Credentials",
        })

    except Exception as e:
      return Response({'message':'fail','error':e,"status": status.HTTP_500_INTERNAL_SERVER_ERROR})


class LogoutAPIView(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes =[JWTAuthentication]
  def post(self, request):
    logout(request)
    return Response({
        "success": True,
        'message': "Successfully Logged out!!!",
        })

class MeAPI(APIView):
  authentication_classes = [JWTAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    try:
      user = CustomUser.objects.filter(email=request.user.email).values('id', 'first_name', 'last_name', 'phone', 'email', 'gender').first()
      data = UserSerializer(user, many=False).data

      if user is not None:
        return Response({
          "success": True,
          "status": status.HTTP_200_OK,
          'message': "Profile retrived successfully!!!",
          "data":data
          })
      else:
        return Response({
          "success": False,
          "status": status.HTTP_404_NOT_FOUND,
          'message': "Invalid user",
          })
    except Exception as e:
      return Response({
          "success": False,
          "status": status.HTTP_404_NOT_FOUND,
          'message': "Invalid user",
          "error": f"the following error are : {e}"
          })