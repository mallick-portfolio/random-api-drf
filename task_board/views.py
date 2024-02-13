from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
  BoardSerializer,
  TaskItemSerializer,
    TaskSerializer,
    BoardUpdateSerializer,
    BoardInvitationSerializer,
    TaskLabelSerializer,
    TaskCommentSerializer,
    TaskAttachmentsSerializer
    )
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from task_board.models import (Board, TaskItem, Task, BoardInvitation,
                                TaskLabel,
                               TaskComment, TaskAttachments)
from django.db import models
import traceback
from accounts.helpers import create_default_task_item
# Create your views here.
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from chat.models import Message
from chat.serializers import MessageSerializer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from accounts.models import CustomUser
from accounts import helpers
from django.conf import settings
from notification.helper import create_notification
from task_board.tasks import email_template
from rest_framework import viewsets


class BoardAPIView(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes = [JWTAuthentication]
  def get(self,request, unique_id=None):
    user = request.user
    if unique_id is not None:
      board = Board.objects.filter(unique_id=unique_id,authorize_users__contains=[user.id]).first()
      if board is not None:

        task_item = TaskItem.objects.filter(board=board).order_by('position')
        serializer = BoardSerializer(board, many=False)
        data = {}
        messages = Message.objects.filter(board=board).order_by('created_at')

        data['board'] = serializer.data
        invited_user = BoardInvitation.objects.filter(board=board)
        data['invited_members'] = BoardInvitationSerializer(invited_user, many=True).data


        data['task_item'] = TaskItemSerializer(task_item, many=True).data

        for t in data['task_item']:
          task = Task.objects.filter(task_item__id=t['id']).order_by('position')
          t['tasks'] = TaskSerializer(task, many=True).data

        data['messages'] = MessageSerializer(messages, many=True).data
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
          }, status=status.HTTP_200_OK)
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
      data['unique_id'] = get_random_string(20).lower()
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

  def put(self, request, unique_id):
    board = Board.objects.filter(unique_id=unique_id, user=request.user).first()
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

  def delete(self,request, unique_id=None):
    user = request.user
    if unique_id is not None:
      board = Board.objects.filter(unique_id=unique_id, user=user).first()
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
      board = Board.objects.filter(unique_id=data['board'], authorize_users__contains=[user.id]).first()
      print("board", board)
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

        data['board'] = board.id

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
            'message': "Serializer error!!!",
            'error': True
          })
      else:
        return Response({
            "success": False,
            'message': "Invalid board id!!!. Failed to create new task item",
            'error': True
          })

    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })

  def put(self, request, pk):
    try:
      data = request.data
      task_item = TaskItem.objects.filter(pk=pk, board__unique_id=data['board']).first()


      if task_item is not None:
        title = data.get('title')
        new_position = data.get('position')
        if title is not None:
          if TaskItem.objects.filter(board__unique_id=data['board'], title=data['title']).exists():
            return Response({
            "success": True,
            "message": "Task item name already exist. Try with another name!!!",
            "error": False
            })
          task_item.title = data['title']
          task_item.save()
        if new_position is not None and task_item.board.user.id == request.user.id:
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

  def get(self, request, pk):
    try:
      task = Task.objects.filter(pk=pk).first()
      if task is not None:
        data = TaskSerializer(task).data
        return Response({
            "success": True,
            'message': "Task details retrived successfully!!!",
            'error': False,
            "data": data
          })
      else:
        return Response({
            "success": False,
            'message': "Task id not found",
            'error': True
          })

    except Exception as e:
      return Response({
        "success": False,
        "error": f'error is {e}'
        })

  def post(self, request):
    try:
      user = request.user
      data = request.data
      task_item = TaskItem.objects.filter(id=data['task_item']).first()
      print("task_item", task_item)
      if task_item is not None:
        task = Task.objects.filter(title=data['title'], task_item=task_item).first()
        print("task", task)
        if task is not None:
          return Response({
            "success": False,
            'message': "Task already exist with this name. Please try with another name!!!",
            'error': True
          })

        max_position = Task.objects.filter(task_item=task_item).aggregate(models.Max('position'))['position__max']
        if max_position is not None:
          data['position'] = max_position + 1
        else:
          data['position'] = 1
        # authorize_users = []
        # authorize_users.append(user.id)
        # data['authorize_users'] = authorize_users
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
          serializer.save(user=user, authorize_users=[self.request.user.id])
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


  def patch(self, request, pk):
    try:
      task = get_object_or_404(Task, pk=pk)
      data = request.data

      if task is not None and str(request.user.id) in task.authorize_users:
        current_task_item = task.task_item
        current_position = task.position
        new_position = data.get('new_position')
        new_task_item = get_object_or_404(TaskItem, id=data.get('task_item'))
        if new_task_item == current_task_item:
          if current_position < new_position:
            tasks_to_update = Task.objects.filter(position__gt=current_position, position__lte=new_position, task_item=current_task_item)
            for t in tasks_to_update:
              t.position -= 1
              t.save()
          elif current_position > new_position:
            tasks_to_update = Task.objects.filter(position__lt=current_position, position__gte=new_position, task_item=current_task_item)
            for t in tasks_to_update:
              t.position += 1
              t.save()
          task.position = new_position
          task.save()
        else:

          tasks_to_update = Task.objects.filter(position__gt=current_position, task_item=current_task_item)
          for t in tasks_to_update:
            t.position -= 1
            t.save()
          tasks_to_update = Task.objects.filter(position__gte=new_position, task_item=new_task_item)
          for t in tasks_to_update:
            t.position += 1
            t.save()
          task.position = new_position
          task.task_item = new_task_item
          task.save()

      return Response({
        "success": True,
        "message": 'Task moved successfully!!!',
        'error': False
      })
    except Exception as e:
      return Response({
        "success": False,
        "error": f'error is {e}'
      })



  def delete(self, request, pk):
    try:
      task = get_object_or_404(Task, pk=pk)
      if task is not None:
        task.delete()
        return Response({
          "success": True,
          "message": 'Task delete successfully!!!',
          'error': False
        })
      else:
        return Response({
          "success": False,
          "message": 'Task delete failed!!!',
          'error': True
        })
    except Exception as e:
      return Response({
        "success": False,
        "error": f'error is {e}'
      })


class BoardMember(APIView):
  def post(self, request, action_type):
    data = request.data
    user = request.user
    invited_user_id = data.get('user_id')
    unique_id = data.get('unique_id')
    try:

      board = Board.objects.filter(unique_id=unique_id, authorize_users__contains=[user.id]).first()
      if action_type == 'invite-board':
        if board is not None:
          invited_user = CustomUser.objects.filter(id=invited_user_id).first()
          board_invite = BoardInvitation.objects.create(board=board, user=invited_user, status='pending')
          data = {}
          data['url'] = f'{settings.FRONT_END_DOMAIN}/account/invite-board-member/?board={board.title}&user={user.first_name}_{user.last_name}&invitation_id={board_invite.id}&unique_id={board.unique_id}'
          data['board'] = board.title
          data['user'] = f'{user.first_name} {user.last_name}'

          notification_message = f"<div>You are invited to the board {board.title} <a href='{data['url']}'>See</a></div>"
          create_notification(user, invited_user, notification_message)



          # email_template.delay(invited_user.email, data,'Board invitations', './email/boardInvitation.html')

          return Response({
              "success": True,
              'message': "Board member invitation successfully",
              'error': False
            })

        else:
          return Response({
              "success": False,
              'message': "Invalid board id",
              'error': True
            })

      elif action_type == 'accept-invitation':
        board_invite = BoardInvitation.objects.filter(id=data['invitation_id'],user=user).first()

        if board_invite is not None and board_invite.board.unique_id == unique_id:
          board_invite.board.authorize_users.append(user.id)
          board_invite.board.save()
          board_invite.delete()

          notification_message = f"<div>{user.first_name} {user.last_name} accept the {board_invite.board.title} board invitation </div>"
          create_notification(user, board_invite.board.user, notification_message)
          return Response({
                "success": True,
                'message': "Invitation accept successfully!!!",
                'error': False
              })
        else:
          return Response({
                "success": False,
                'message': "Invalid board id or user!!!",
                'error': True
              })
      elif action_type == 'reject-invitation':
        board_invite = BoardInvitation.objects.filter(id=data['invitation_id']).first()
        if board_invite is not None:
          board_invite.delete()
          return Response({
              "success": True,
              "reject": True,
              'message': "Invitation reject successfully!!!",
              'error': False
            })
        else:
          return Response({
                "success": False,
                'message': "Invalid board id or user!!!",
                'error': True
              })
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })


class TaskLabelViewSet(viewsets.ModelViewSet):

  queryset = TaskLabel.objects.all()
  serializer_class = TaskLabelSerializer
  permission_classes = [IsAuthenticated]
  authentication_classes = [JWTAuthentication]


class TaskCommentAPI(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes = [JWTAuthentication]
  def post(self, request):
    try:
      user = request.user
      data = request.data
      data['comment_type'] = 'text'
      task = Task.objects.filter(id=data['task']).first()
      if task is not None:
        # data['task'] = task.id
        serializer = TaskCommentSerializer(data=data)
        if serializer.is_valid():
          serializer.save(user=self.request.user)
          return Response({
            "success": True,
            'message': "Comment added!!!",
            'error': False
          })

        else:
          return Response({
          "success": False,
          'message': "Invalid data",
          'error': True,
        })

      else:
        return Response({
          "success": False,
          'message': "Invalid task id!!!. Failed to create new task",
          'error': True
        })
    except Exception as e:
      return Response({
        "success": False,
        "error": f'error is {e}'
        })


# assign member for particular task
class AssignTaskMember(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes = [JWTAuthentication]
  def post(self, request, task_id):
    try:
      task = Task.objects.filter(id=task_id).first()
      data = request.data

      if task is not None:
        user = CustomUser.objects.filter(id=data['user']).first()
        if user is not None:
          task.authorize_users.append(data['user'])
          task.save()
          return Response({
              "success": True,
              'message': "Assign member added!!!",
              'error': False
            })
        else:
          return Response({
              "success": False,
              'message': "Invalid member!!!",
              'error': True
            })
      else:
        return Response({
            "success": False,
            'message': "Failed to assign member!!!",
            'error': True
          })
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
          })

class CommentAttachmentsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        try:
            data = request.data
            images = data.getlist('image')
            files = data.getlist('file')
            task_id = data.get('task')

            task = Task.objects.get(id=task_id)
            if task is not None:
                comment = TaskComment.objects.create(task=task, user=request.user, comment_type="media")

                if comment is not None:
                    for image in images:
                        serializer = TaskAttachmentsSerializer(data={"comment": comment.id, 'image': image, "media_type": 'image', })
                        if serializer.is_valid():
                            serializer.save()
                    for media_file in files:

                        serializer = TaskAttachmentsSerializer(data={"comment": comment.id, 'media_file': media_file,"media_type": 'file',})
                        if serializer.is_valid():
                            serializer.save()
                        else:
                          print(serializer.errors)

                    return Response({
                        "success": True,
                        'message': "Files uploaded!!!",
                        'error': False,
                        })
            else:
                return Response({
                    "success": False,
                    'message': "Invalid task id",
                    'error': True
                    })
        except Exception as e:
            return Response({
                "error": f'Error is {e}',
                'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
                })

