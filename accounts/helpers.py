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
    current_time = timezone.now()
    time_difference = current_time - otp_send_time
    if time_difference > timedelta(minutes=5):
        return True
    else:
        return False




def email_template(email,data, subject, template):
    print("email", email, data, subject, template)
    try:
        message = render_to_string(template, {
            'email' : email,
            "data": data
        })
        send_email = EmailMultiAlternatives(subject, '', to=[email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
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