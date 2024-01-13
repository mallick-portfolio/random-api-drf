from django.shortcuts import render
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MessageAttachments, Message
from .serializers import MessageAttachmentsSerializer, MessageSerializer
import traceback
from task_board.models import Board
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer




class MessageAttachmentsView(APIView):
    def post(self, request):
        try:
            data = request.data
            media_type = data['media_type']
            images = data.getlist('image')
            files = data.getlist('file')
            board_id = data.get('board_id')
            board = Board.objects.get(id=board_id)
            if board is not None:
                message = Message.objects.create(board=board, sender=request.user, message_type="media")

                if message is not None:
                    for image in images:
                        serializer = MessageAttachmentsSerializer(data={"message": message.id, 'image': image, "media_type": media_type, })
                        if serializer.is_valid():
                            serializer.save()
                    for media_file in files:
                        serializer = MessageAttachmentsSerializer(data={"message": message.id, 'media_file': media_file,"media_type": media_type,})
                        if serializer.is_valid():
                            serializer.save()


                    messageData = MessageSerializer(message).data
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(
                        f'board_{board.unique_id}',
                        {
                            'type': 'chat_message',
                            'message': messageData
                        }
                    )
                    return Response({
                        "success": True,
                        'message': "Files uploaded!!!",
                        'error': False,
                        "data": messageData
                        })
            else:
                return Response({
                    "success": False,
                    'message': "Invalid Board id",
                    'error': True
                    })
        except Exception as e:
            return Response({
                "error": f'Error is {e}',
                'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
                })

