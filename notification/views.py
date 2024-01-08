from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import traceback
from notification.serializers import NotificationSerializer
from notification.models import Notification
from accounts.models import CustomUser
# Create your views here.



class NotificationAPIView(APIView):
  permission_classes = [IsAuthenticated]
  authentication_classes = [JWTAuthentication]
  def get(self, request):
    try:
      user = CustomUser.objects.filter(id=request.user.id).first()
      if user is not None:
        payload = Notification.objects.filter(receiver=user).order_by('created_at')
        data = NotificationSerializer(payload, many=True).data
      return Response({
        "success": True,
        "status": status.HTTP_200_OK,
        'message': "Invalid Credentials",
        "data": data
      })
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })