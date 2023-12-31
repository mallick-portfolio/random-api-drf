from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BoardSerializer, TaskItemSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class BoardAPIView(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request):
    try:
      user = request.user
      if user.is_authenticated:
        print(user)
        serializer = BoardSerializer(data=request.data)
        if serializer.is_valid():
          print(serializer)
          serializer.save()
          return Response({
            "success": True,
            "status": status.HTTP_201_CREATED,
            'message': "Board created successfully!!!",
          })
        else:
          return Response({
            "success": False,
            "status": status.HTTP_400_BAD_REQUEST,
            'message': "Invalid Credentials",
            "error": serializer.errors
          })
    except Exception as e:
      return Response({
          "success": False,
          "error": e
        })