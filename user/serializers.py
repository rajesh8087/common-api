from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_recursive.fields import RecursiveField
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.translation import gettext_lazy as _
from user.utils import send_password_reset_email, check_contact, check_pass, check_name
import re
from company.validator import contact_validator
from .models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {"no_active_account": _("Invalid email or password.")}

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # customizing claims
        token["user_role"] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, write_only=True
    )
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)

    # ROLE_CHOICES = (
    #     ("Super Admin", "Super Admin"),
    #     ("Franchise Admin", "Franchise Admin"),
    #     ("Admin", "Admin"),
    #     ("Client", "Client"),
    #     ("Manager", "Manager"),
    #     ("Assistant Manager", "Assistant Manager"),
    #     ("Associate", "Associate"),
    # )
    # email = serializers.EmailField(validators=[UniqueEmailValidator()], required=True)
    # name = serializers.CharField(max_length=50, required=True)
    # employee_id = serializers.IntegerField(
    #     validators=[UniqueValidator(queryset=User.objects.all())],
    #     required=True,
    #     min_value=1,
    # )
    # contact = serializers.IntegerField(
    #     validators=[UniqueValidator(queryset=User.objects.all()), contact_validator],
    #     required=True,
    #     min_value=1,
    # )
    # creator = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(), required=True
    # )
    # reporting_to = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(), required=True
    # )

    class Meta:
        model = User
        fields = [
            "name",
            "email",
            "employee_id",
            "contact",
            "password",
            "confirm_password",
            "role",
            "creator",
            "reporting_to",
        ]
        extra_kwargs = {
            "creator": {
                "error_messages": {"does_not_exist": "Creator does not exists."}
            }
        }

    def create(self, validated_data):
        # print(data)
        password = validated_data["password"]
        confirm_password = validated_data.pop("confirm_password")
        name = validated_data["name"]
        contact = str(validated_data["contact"])

        if not re.search(check_name, name):
            raise serializers.ValidationError("Name must be only characters")

        if not re.match(check_pass, password):
            raise serializers.ValidationError(
                "Password must be 8 characters long with one uppercase letter,one lowercase letter, one digit and one special Character"
            )

        if password != confirm_password:
            raise serializers.ValidationError(
                {"password": "Password and confirm password doesn't match."}
            )

        user = User.objects.create_user(**validated_data)

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "employee_id", "contact"]


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "email", "contact"]

    # def update(self, instance, validated_data):
    #     instance.save(**validated_data)
    #     return instance


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")
        user = self.context.get("user")
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match"
            )
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print("Encoded UID", uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print("Password Reset Token", token)
            link = "http://localhost:3000/api/user/reset/" + uid + "/" + token

            body = "Click Following Link to Reset Your Password " + link
            data = {
                "subject": "Reset Your Password",
                "body": body,
                "to_email": user.email,
            }
            send_password_reset_email(data)
            return attrs
        else:
            raise serializers.ValidationError("You are not a Registered User")


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            password2 = attrs.get("password2")
            uid = self.context.get("uid")
            token = self.context.get("token")
            if password != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't match"
                )
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError("Token is not Valid or Expired")
            user.set_password(password)
            user.save()
            return attrs

        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError("Token is not Valid or Expired")


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "employee_id", "role", "employees"]


# Hierarchy from top to bottom
"""
        SuperAdmin -> (Suhas Sir)
            |
        Franchise Admin -> (Tanmay)
            |
        Admin/Partner -> (Bipin)
            |
          Manager -> (Rajesh)
            |
        Assistant Manager -> (Pranay)
            |
        Associate -> (Bhavesh)
"""

# Fetch Hierarchy from --> Lower to Upper i.e ( Bhavesh(Associate) ---> Suhas(Super Admin) )


class FetchAncestorEmployeeSerializer(serializers.ModelSerializer):
    reporting_to = RecursiveField(allow_null=True)

    class Meta:
        model = User
        fields = ["name", "employee_id", "role", "reporting_to"]


# Fetch Lower --> Upper to Lower i.e ( Suhas(Super Admin) --->  Bhavesh(Associate) )
class FetchChildEmployeeSerializer(serializers.ModelSerializer):
    employees = RecursiveField(allow_null=True, many=True)

    class Meta:
        model = User
        fields = ["name", "employee_id", "role", "employees"]
