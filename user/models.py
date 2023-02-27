from django.db.models import *
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.core.validators import validate_email
from django.utils import timezone
from company.models import Company

timezone.activate('Asia/Kolkata')

class User(AbstractBaseUser, PermissionsMixin):
    SUPER_ADMIN = "Super Admin"
    FRANCHISE_ADMIN = "Franchise Admin"
    ADMIN = "Admin"
    MANAGER = "Manager"
    ASSISTANT_MANAGER = "Assistant Manager"
    ASSOCIATE = "Associate"

    CHOICES = (
        (SUPER_ADMIN, "Super Admin"),
        (FRANCHISE_ADMIN, "Franchise Admin"),
        (ADMIN, "Admin"),
        (MANAGER, "Manager"),
        (ASSISTANT_MANAGER, "Assistant Manager"),
        (ASSOCIATE, "Associate")
    )

    email = EmailField(unique=True, db_index=True, validators=[validate_email])
    name = CharField(max_length=50)
    employee_id = IntegerField(unique=True, )

    contact = PositiveBigIntegerField()
    role = CharField(choices=CHOICES, max_length=50, default=SUPER_ADMIN)
    is_active = BooleanField(default=True)

    is_admin = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    assigned_companies = ManyToManyField(Company, blank=True, related_name="assigned_companies", default=None)

    creator = ForeignKey("user.User", default=None, on_delete=DO_NOTHING, related_name="created_by", null=True)
    reporting_to = ForeignKey("user.User", default=None, on_delete=DO_NOTHING, related_name="reports_to", null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'employee_id', 'contact']
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    

    @classmethod
    def update_data(self,validate_data,pk):
        User.objects.filter(id=pk).update(**validate_data)

