from django.db.models import *
from django.forms import ValidationError
from django.utils import timezone
from django.core.validators import validate_email, FileExtensionValidator, MaxValueValidator
from .validator import gst_validator,pan_validator,contact_validator


# Create your models here.

def validate_file_size(value):
    filesize = value.size
    
    if filesize > 30 * 1024 * 1024:
        raise ValidationError("The maximum file size that can be uploaded is 30MB")

class Company(Model):
    name = CharField(max_length=50, unique=True, null=True,error_messages={'unique': 'name already exist'})
    email = EmailField(unique=True,validators=[validate_email], error_messages={'unique': 'Email already exist'})
    contact = PositiveBigIntegerField(default=9999999999,validators=[contact_validator])

    contact_person = CharField(max_length=50, default="")
    address = CharField(max_length=200, default="default address")
    gst = CharField(max_length=15, default="07AAWFR0503R1ZK",validators=[gst_validator])
    pan_no = CharField(max_length=15, default="AABCI6154K",validators=[pan_validator])

    owners_name = CharField(max_length=50, default="")
    owners_email = EmailField(max_length=50, default="")
    owners_birth_date = DateField(default=timezone.now, blank=True, null=True)

    fees = IntegerField(default=100000)
    documents = FileField(
        upload_to="media/",
        default="N/A",
        null=True,
        blank=True,
        # validators=[FileExtensionValidator(allowed_extensions=['pdf', 'csv', 'xls', 'xlsx']),MaxValueValidator(30 * 1024 * 1024)]
        validators=[validate_file_size]
    )
    creator = ForeignKey("user.User", default=None, on_delete=DO_NOTHING, related_name="company_created_by", null=True)
    is_deleted = BooleanField(default=False)

    def __str__(self):
        return self.name

    @classmethod
    def create_company(self, validated_data, creator):
        company = Company.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            contact_person=validated_data['contact_person'],
            contact=validated_data['contact'],
            address=validated_data['address'],
            gst=validated_data['gst'],
            pan_no=validated_data['pan_no'],
            owners_name=validated_data['owners_name'],
            owners_email=validated_data['owners_email'],
            fees=validated_data['fees'],
            owners_birth_date=validated_data['owners_birth_date'],
            documents=validated_data['documents'],
            creator=creator

        )
        return company

    @classmethod
    def update_data(self, validate_data, pk):
        Company.objects.filter(id=pk).update(**validate_data)


    
