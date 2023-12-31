from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BoardSerializer, TaskItemSerializer, TaskSerializer
from rest_framework.permissions import IsAuthenticated
from task_board.models import Board, TaskItem, Task
# Create your views here.

class BoardDetailsAPIView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, id):
    board = Board.objects.filter(id=id, authorize_users__contains=[request.user.id]).first()
    if board is not None:
      data = BoardSerializer(board,many=False).data
      return Response({
            "success": True,
            "status": status.HTTP_200_OK,
            'message': "Board retrived successfully!!!",
            'data': data
          })
    else:
      return Response({
            "success": False,
            "status": status.HTTP_404_NOT_FOUND,
            'message': "Board not found",
          })


class BoardAPIView(APIView):

  permission_classes = [IsAuthenticated]
  def get(self,request):
    user = request.user
    board = Board.objects.filter(authorize_users__contains=[request.user.id])
    serializer = BoardSerializer(board, many=True)
    return Response({
          "success": True,
          "status": status.HTTP_201_CREATED,
          'message': "Board retrived successfully!!!",
          'data': serializer.data
        })



  def post(self, request):
    try:
      data = request.data
      data['user'] = request.user.id
      data['authorize_users'] = [request.user.id]
      serializer = BoardSerializer(data=data)
      if serializer.is_valid():
        serializer.save()
        return Response({
          "success": True,
          "status": status.HTTP_201_CREATED,
          'message': "Board created successfully!!!",
          'data': serializer.data
        })
      else:
        return Response({
          "success": False,
          "status": status.HTTP_400_BAD_REQUEST,
          'message': "Invalid Credentials",
          "error": serializer.errors
        })
    except Exception as e:
      return Response(str(e), status=status.HTTP_404_NOT_FOUND, )