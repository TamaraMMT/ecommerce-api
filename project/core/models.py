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
        if not email:  # Check for empty email
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
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    password = models.CharField(max_length=366)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = Manager()

    USERNAME_FIELD = 'email'
