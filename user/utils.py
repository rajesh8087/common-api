from rest_framework import status
from rest_framework.response import Response
from django.core.mail import EmailMessage, send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from api import settings
import os
import re


def send_password_reset_email(data):
    email = EmailMessage(
        subject=data["subject"],
        body=data["body"],
        from_email=os.environ.get("EMAIL_FROM"),
        to=[data["to_email"]],
    )
    email.send()


check_pass = re.compile(
    "^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])"
)

check_name = r"^[a-zA-Z ]*$"

check_contact = r"^\d{10}$"
