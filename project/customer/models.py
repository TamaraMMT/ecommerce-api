"""
Models customer users
"""
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.db.models.signals import post_save
from django.dispatch import receiver

from shortuuid.django_fields import ShortUUIDField 


class CustomerManager(BaseUserManager):
    """
    Custom manager for Customer model
    """
    def create_customer(self, email, password=None, **others_fields):
        if not email:
            raise ValueError("The email cannot be empty")
        email = self.normalize_email(email)
        customer = self.model(
                    email=email,
                    is_active=True,
                    **others_fields)
        customer.set_password(password)
        customer.save(using=self._db)

        return customer


class Customer(AbstractBaseUser):
    """customer users"""
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    pid = ShortUUIDField(
        unique=True, length=10, max_length=20)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return (f"{self.email}")


class Profile(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    customeruser = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True
    )
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (f"{self.firstname} {self.lastname}")


@receiver(post_save, sender=Customer)
def create_customer_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(customeruser=instance)
