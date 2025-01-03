from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.conf import settings

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create and return a regular user with an email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with an email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Remove the username field
    name = models.CharField(max_length=199, null=True)
    email = models.EmailField(unique=True, null=True)

    # Use email as the unique identifier for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No need for username as it is removed

    # Link the custom manager to the User model
    objects = UserManager()

    def __str__(self):
        return self.email
    

class VIPUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vip_profile'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def name(self):
        return self.user.name

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return f"{self.name} ({self.email})"


class ChatData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.CharField(max_length=999991)
    response = models.CharField(max_length=999991)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
