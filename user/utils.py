from django.core.mail import EmailMessage
import os
import re
from django.core.mail import send_mail
from api.settings import EMAIL_HOST_USER
from rest_framework.response import Response
from rest_framework import status


def send_password_reset_email(data):
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


check_pass = re.compile("^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])")

check_name = r'^[a-zA-Z ]*$'

check_contact = r'^\d{10}$'