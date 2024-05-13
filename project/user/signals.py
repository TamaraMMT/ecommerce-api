from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, UserProfile


@receiver(post_save, sender=User)
def create_userprofile(sender, instance, created, *args, **kwargs):
    """
    Creates a UserProfile for a newly created User.
    """
    if created and not instance.is_superuser:
        UserProfile.objects.create(user=instance)
