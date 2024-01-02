from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (BoardSerializer, TaskItemSerializer, TaskSerializer, BoardUpdateSerializer)
from rest_framework.permissions import IsAuthenticated
from task_board.models import Board, TaskItem, Task
# Create your views here.



class BoardAPIView(APIView):

  permission_classes = [IsAuthenticated]
  http_method_names = [
    'get',
    'post',
    'put',
    'delete',
    'head',
    'options',
    ]
  def get(self,request, pk=None):
    user = request.user
    if pk is not None:
      board = Board.objects.filter(pk=pk,authorize_users__contains=[user.id]).first()
      serializer = BoardSerializer(board, many=False)
      return Response({
            "success": True,
            "status": status.HTTP_201_CREATED,
            'message': "Board details retrived successfully!!!",
            'data': serializer.data
          })
    else:
      board = Board.objects.filter(authorize_users__contains=[user.id])
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

  def put(self, request, pk):
    board = Board.objects.filter(pk=pk, user=request.user).first()
    if board is not None:
      serializer = BoardUpdateSerializer(board, data=request.data, partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response({
              "success": True,
              "status": status.HTTP_200_OK,
              'message': "Board updated",
              "data": serializer.data
            })
    else:
      return Response({
            "success": False,
            "status": status.HTTP_400_BAD_REQUEST,
            'message': "Invalid Credentials",
          })

  def delete(self,request, pk=None):
    user = request.user
    if pk is not None:
      board = Board.objects.filter(pk=pk, user=user).first()
      if board is not None:
        board.delete()
        return Response({
            "success": True,
            "status": status.HTTP_200_OK,
            'message': "Board deleted successfully!!!",
          })
      else:
        return Response({
            "success": False,
            "status": status.HTTP_404_NOT_FOUND,
            'message': "Invalid id!!!",
          })


class TaskItemAPI(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request):
    pass

