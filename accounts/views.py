from django.shortcuts import render
from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
      return Response({'message':'fail','error':e,"status": status.HTTP_400_BAD_REQUEST})
