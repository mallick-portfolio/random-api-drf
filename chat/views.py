from django.shortcuts import render

# Create your views here.
# views.py
from rest_framework.parsers import MultiPartParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MessageAttachments
from .serializers import MessageAttachmentSerializer

class MessageAttachmentUploadView(APIView):
    parser_classes = [MultiPartParser, FileUploadParser]

    def post(self, request, message_id):
        print(request.FILES)
        message_attachment_data = {'message': message_id, 'file': request.data.get('file')}
        serializer = MessageAttachmentSerializer(data=message_attachment_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
