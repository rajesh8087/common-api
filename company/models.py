from django.db.models import *
from django.utils import timezone

# Create your models here.

class Company(Model):
    name = CharField(max_length=50, unique=True, null=True)
    email = EmailField(unique=True)
    contact = PositiveBigIntegerField(default=9999999999)

    contact_person = CharField(max_length=50, default="")
    address = CharField(max_length=200, default="default address")
    gst = CharField(max_length=15, default="07AAWFR0503R1ZK")
    pan_no = CharField(max_length=15, default="AABCI6154K")

    owners_name = CharField(max_length=50, default="")
    owners_email = EmailField(max_length=50, default="")
    owners_birth_date = DateField(default=timezone.now, blank=True, null=True)

    fees = IntegerField(default=100000)
    documents = FileField(
        upload_to="media/",
        default="N/A",
        null=True,
        blank=True,
    )
    creator = ForeignKey("user.User", default=None, on_delete=DO_NOTHING, related_name="company_created_by", null=True)
    is_deleted = BooleanField(default=False)

    def __str__(self):
        return self.name


    @classmethod
    def create_company(self,validated_data,creator):
        company = Company.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            contact_person = validated_data['contact_person'],
            contact =  validated_data['contact'],
            address =  validated_data['address'],
            gst =  validated_data['gst'],
            pan_no =  validated_data['pan_no'],
            owners_name =  validated_data['owners_name'],
            owners_email =  validated_data['owners_email'],
            fees =  validated_data['fees'],
            owners_birth_date =  validated_data['owners_birth_date'],
            documents = validated_data['documents'],
            creator= creator
         
        )
        return company

    @classmethod
    def update_data(self,validate_data,pk):
        Company.objects.filter(id=pk).update(**validate_data)