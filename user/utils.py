from django.core.mail import EmailMessage
import os
import re
from django.core.mail import send_mail
from api.settings import EMAIL_HOST_USER
from rest_framework.response import Response
from rest_framework import status


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
          subject=data['subject'],
          body=data['body'],
          from_email=os.environ.get('EMAIL_FROM'),
          to=[data['to_email']]
        )
        email.send()


def send_registration_email(user):
        try:
          subject = 'User Credentials'
          message = f'Dear {user[0].name},\n\nThank you for registering on our website.Here are your login credentials , username{user[0].email},password{user[1]}'
          from_email = EMAIL_HOST_USER
          recipient_list = [user[0].email]
          send_mail(subject, message, from_email, recipient_list)
         
        except Exception as e:
             print(e)
             return Response("mail not send", status=status.HTTP_400_BAD_REQUEST)
        
        
check_gst = re.compile("^[0-9]{2}[A-Z]{5}[0-9]{4}" + "[A-Z]{1}[1-9A-Z]{1}" + "Z[0-9A-Z]{1}$")

check_pan = re.compile("[A-Z]{5}[0-9]{4}[A-Z]{1}")

check_pincode = re.compile("[A-Z]{5}[0-9]{4}[A-Z]{1}")

check_contact = r'^\d{10}$'

check_email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

check_pass = re.compile("^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])")

check_name = r'^[a-zA-Z ]*$'