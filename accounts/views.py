from django.shortcuts import render
from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from . import helpers
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
          "success": True,
          "status": status.HTTP_400_BAD_REQUEST,
          'message': "Registration failed",
          'error': serializer.errors
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
          "status": status.HTTP_400_BAD_REQUEST,
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
          "status": status.HTTP_200_OK,
          'message': "Login successfull!!!",
          "token": token
        })
      else:
        return Response({
          "success": False,
          "status": status.HTTP_401_UNAUTHORIZED,
          'message': "Invalid Credentials",
        })

    except Exception as e:
      return Response({'message':'fail','error':e,"status": status.HTTP_500_INTERNAL_SERVER_ERROR})


class LogoutAPIView(APIView):
  def post(self, request):
    logout(request)
    return Response({
        "success": True,
        "status": status.HTTP_200_OK,
        'message': "Successfully Logged out!!!",
        })

