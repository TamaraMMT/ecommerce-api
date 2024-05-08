"""
Models Databases
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class Manager(BaseUserManager):
    """Manager user"""

    def create_user(self, email, password=None, **others_fields):
        if not email:
            raise ValueError("The email cannot be empty")
        user = self.model(email=self.normalize_email(email), **others_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create super user and return"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User"""
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=366)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = Manager()

    USERNAME_FIELD = 'email'


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='userprofile'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    shipping_address = models.TextField(blank=True)
    billing_address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
