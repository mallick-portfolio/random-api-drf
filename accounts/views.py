from django.shortcuts import render
from .serializers import RegistrationSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from . import helpers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import CustomUser
# Create your views here.


class RegistrationAPIView(APIView):
  def post(self, request):
    serializer = RegistrationSerializer(data=request.data)
    try:
      if serializer.is_valid():
        serializer.save()
        return Response({
          "success": True,
          "status": status.HTTP_201_CREATED,
          'message': "Registration successfull!!!"
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