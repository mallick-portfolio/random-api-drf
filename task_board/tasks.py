

from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import  EmailMultiAlternatives
from rest_framework.response import Response
import traceback


@shared_task
def email_template(email,data, subject, template):
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


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


