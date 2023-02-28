from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, name, password, employee_id, contact, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            employee_id=employee_id,
            contact=contact,
            **extra_fields
        )
        pass_email = password
        user.set_password(password)
        user.save(using=self._db)
        return user,pass_email
    
    
    def create_superuser(self, email, name, password, employee_id, contact, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, name, password, employee_id, contact, **extra_fields)