from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (BoardSerializer, TaskItemSerializer, TaskSerializer, BoardUpdateSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from task_board.models import Board, TaskItem, Task
from django.db import models
import traceback
from accounts.helpers import create_default_task_item
# Create your views here.



class BoardAPIView(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes = [JWTAuthentication]
  def get(self,request, pk=None):
    user = request.user
    if pk is not None:
      board = Board.objects.filter(pk=pk,authorize_users__contains=[user.id]).first()
      if board is not None:

        task_item = TaskItem.objects.filter(board=board).order_by('position')
        serializer = BoardSerializer(board, many=False)
        data = {}
        data['board'] = serializer.data
        data['task_item'] = TaskItemSerializer(task_item, many=True).data

        for t in data['task_item']:
          task = Task.objects.filter(task_item__id=t['id'])
          t['tasks'] = TaskSerializer(task, many=True).data

        return Response({
              "success": True,
              'message': "Board details retrived successfully!!!",
              'data': data
            },status=status.HTTP_200_OK)
      else:
        return Response({
            "success": False,
            'message': "Board not found with the given id!!!",
            'error': False
          }, status=status.HTTP_404_NOT_FOUND)
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

      serializer = BoardSerializer(data=data)
      if serializer.is_valid():
        board = serializer.save(user=self.request.user, authorize_users=[self.request.user.id])
        create_default_task_item(board=board, user=request.user)
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
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })

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

  def post(self, request):
    try:
      user = request.user
      data = request.data
      board = Board.objects.filter(id=data['board'], authorize_users__contains=[user.id]).first()
      if board is not None:
        task_item = TaskItem.objects.filter(title=data['title'], board=board).first()
        if task_item is not None:
          return Response({
            "success": False,
            'message': "A task item already exit with this name in this board. Please try with another name.",
            "error": True
          })

        max_position = TaskItem.objects.filter(board=board).aggregate(models.Max('position'))['position__max']
        if max_position is not None:
          data['position'] = max_position + 1
        else:
          data['position'] = 1

        serilizer = TaskItemSerializer(data=data)
        if serilizer.is_valid():
          serilizer.save(user=request.user)
          return Response({
            "success": True,
            'message': "New task item created successfully",
            "data": serilizer.data
          }, status=status.HTTP_201_CREATED)
      else:
        return Response({
            "success": False,
            'message': "Invalid board id!!!. Failed to create new task item",
            'error': True
          })

    except Exception as e:
      return Response({
        "success": False,
        "error": f'error is {e}'
          })

  def put(self, request, pk):
    try:
      data = request.data
      task_item = TaskItem.objects.filter(pk=pk, board__id=data['board']).first()

      if task_item is not None:
        title = data.get('title')
        new_position = data.get('position')
        if title is not None:
          if TaskItem.objects.filter(board__id=data['board'], title=data['title']).exists():
            return Response({
            "success": True,
            "message": "Task item name already exist. Try with another name!!!",
            "error": False
            })
          task_item.title = data['title']
          task_item.save()
        if new_position is not None:
          current_position = task_item.position

          if current_position < new_position:
            TaskItem.objects.filter(position__gt=current_position, position__lte=new_position, board=task_item.board).update(position=models.F('position') - 1)
          elif current_position > new_position:
            TaskItem.objects.filter(position__lt=current_position, position__gte=new_position, board=task_item.board).update(position=models.F('position') + 1)

          task_item.position = new_position
          task_item.save()

        return Response({
          "success": True,
          "message": "Task item update successfully!!!",
          "error": False
          })
      else:
        return Response({
          "success": False,
          "message": "Invalid task item id",
          'error': True
          })

    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })

  def delete(self, request, pk):
    try:
      task_item = TaskItem.objects.filter(pk=pk).first()
      board = Board.objects.filter(id=task_item.board.id, authorize_users__contains=[request.user.id])
      current_position = task_item.position

      if board and task_item:
        task_item.delete()
        TaskItem.objects.filter(position__gt=current_position, board=task_item.board).update(position=models.F('position') - 1)


        return Response({
            "success": True,
            "message": "Task item deleted successfully!!!",
            'error': False
            })
      else:
        return Response({
            "success": False,
            "message": "Invalid task item id",
            'error': True
            })
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })


class TaskAPI(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes = [JWTAuthentication]

  def post(self, request):
    try:
      user = request.user
      data = request.data
      task_item = TaskItem.objects.filter(id=data['task_item']).first()
      if task_item is not None:
        task = Task.objects.filter(title=data['title'], task_item=task_item).first()
        if task is not None:
          return Response({
            "success": False,
            'message': "Task already exist with this name. Please try with another name!!!",
            'error': True
          })


        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
          serializer.save(user=user)
          return Response({
            "success": True,
            'message': "Task created successfully!!!!",
            'error': True
          })
        else:
          return Response({
            "success": False,
            'message': "Failed to create new task. Something want wrong",
            'error': True
          })
      else:
        return Response({
          "success": False,
          'message': "Invalid task item id!!!. Failed to create new task",
          'error': True
        })
    except Exception as e:
      return Response({
        "success": False,
        "error": f'error is {e}'
          })

