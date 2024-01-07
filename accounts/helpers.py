from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response

from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string
import string
import random
from datetime import datetime, timedelta
from django.utils import timezone
from task_board.models import TaskItem
import traceback

def compare_minute(otp_send_time):
    print(otp_send_time)
    current_time = timezone.now()
    print(current_time)
    time_difference = current_time - otp_send_time
    if time_difference > timedelta(minutes=5):
        return True
    else:
        return False


def send_otp_email(email,data, subject, template):
    try:
        pass
    except Exception as e:
      return Response({
          "error": f'Error is {e}',
          'trackback': "".join(traceback.format_exception(type(e), e, e.__traceback__))
        })

def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def create_default_task_item(board, user):
    default_item = ['Todo', 'In Progress', "Done"]
    for index, val in enumerate(default_item):
        TaskItem.objects.create(title=val, board=board,user=user, position=index+1)
        print(index, val)