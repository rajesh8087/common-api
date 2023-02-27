import threading
from django.core.mail import EmailMessage
import os
import re


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

# class UserCreationThread(threading.Thread):
#     def __init__(self, password, role, name, email, host):
#         super().__init__()
#         self.subject = "CFO Services/Visit Report Tool"
#         self.sender = settings.EMAIL_HOST_USER
#         self.password = password
#         self.role = role
#         self.name = name
#         self.email = email
#         self.host = host
#         self.stop_event = threading.Event()

#     def run(self):
#         data = {
#             "link": self.host,
#             "role": self.role,
#             "name": self.name,
#             "password": self.password,
#             "email": self.email,
#         }
       
#         # email.send()
#         data.send()

#         self.stop_event = threading.Event()


check_gst = re.compile("^[0-9]{2}[A-Z]{5}[0-9]{4}" + "[A-Z]{1}[1-9A-Z]{1}" + "Z[0-9A-Z]{1}$")

check_pan = re.compile("[A-Z]{5}[0-9]{4}[A-Z]{1}")

check_pincode = re.compile("[A-Z]{5}[0-9]{4}[A-Z]{1}")

check_contact = r'^\d{10}$'

check_email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

check_pass = re.compile("^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])")

check_name = r'^[a-zA-Z ]*$'