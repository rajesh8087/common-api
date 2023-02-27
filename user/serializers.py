from user.utils import Util
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from rest_framework import serializers
import re
from user.utils import check_contact, check_pass, check_name

User = get_user_model()

class UniqueEmailValidator:
    def __call__(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already in use.")

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    ROLE_CHOICES = (
        ("Super Admin", "Super Admin"),
        ("Franchise Admin", "Franchise Admin"),
        ("Admin", "Admin"),
        ("Client", "Client"),
        ("Manager", "Manager"),
        ("Assistant Manager", "Assistant Manager"),
        ("Associate", "Associate"),
    )
    email = serializers.EmailField(validators=[UniqueEmailValidator()], required=True)
    name = serializers.CharField(max_length=50, required=True)
    employee_id = serializers.IntegerField(validators=[UniqueValidator(queryset=User.objects.all())], required=True, min_value=1)
    contact = serializers.IntegerField(validators=[UniqueValidator(queryset=User.objects.all())], required=True, min_value=1)
    role = serializers.ChoiceField(choices=ROLE_CHOICES, required=True)
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    reporting_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['name', 'email', 'employee_id', 'contact', 'password', 'confirm_password', 'role', 'creator', 'reporting_to']


    def create(self, validated_data):
        
        password = validated_data['password']
        confirm_password = validated_data.pop('confirm_password')

        name = validated_data['name']
        employee_id = validated_data['employee_id']
        contact = str(validated_data['contact'])
        email = validated_data['email']
        
    
        if User.objects.filter(employee_id=employee_id).exists():
            raise serializers.ValidationError("Employee_id already exist")

        # Check if contact is unique
        if User.objects.filter(contact=contact).exists():
            raise serializers.ValidationError("Contact already exist")

        # Check if email is unique
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exist")
        
        if not re.search(check_name , name):
            raise serializers.ValidationError("Name must be only characters")

        
        if not re.search(check_contact, contact):
            raise serializers.ValidationError("Please Enter a valid Contact Number ")

        if not re.match(check_pass, password):
            raise serializers.ValidationError("Password must be 8 characters long with one uppercase letter,one lowercase letter, one digit and one special Character")

        if password != confirm_password:
            raise serializers.ValidationError({"password": "Password and confirm password doesn't match."})
        
        
        user=User.objects.create_user(**validated_data)
        return user
        
 

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['email', 'password']


class GetAllUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','email','contact']

    

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.set_password(password)
        user.save()
        return attrs


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/' + uid + '/' + token
           
            body = 'Click Following Link to Reset Your Password ' + link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('You are not a Registered User')


class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("Password and Confirm Password doesn't match")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError('Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')
