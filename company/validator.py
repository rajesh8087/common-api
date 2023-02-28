import re
from django.core.exceptions import ValidationError
from company.models import Company
from user.utils import check_contact,check_email_regex,check_gst,check_pan
from api.settings import FILE_UPLOAD_MAX_MEMORY_SIZE


def validate_company_documents_size(file):
    if file.size > FILE_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError("company documents size must be less than 30MB")


def validate_company_name(name):
    if Company.objects.filter(name=name).exists():
        raise ValidationError("company name already exists")


def validate_company_email(email):
    if Company.objects.filter(email=email).exists():
        raise ValidationError("company with this email already exists")


def validate_email(email):
    if not re.search(check_email_regex, email):
        raise ValidationError("Please Enter a valid Email Id")


def validate_gst(gst):
    if not re.search(check_gst, gst):
        raise ValidationError("Please Enter a valid GST Number")


def validate_pan(pan_no):
    if not re.search(check_pan, pan_no):
        raise ValidationError("Please Enter a valid PAN Number")


def validate_contact(contact): 
    if not re.search(check_contact, contact):
        raise ValidationError("Please Enter a valid contact Number")
        

def validate_company(contact, email, name, documents=None):
    validate_company_name(name)
    validate_company_email(email)
    validate_email(email)
    validate_contact(contact)
    if documents:
        validate_company_documents_size(documents)
