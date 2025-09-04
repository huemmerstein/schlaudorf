"""Signal handlers for the chat app."""
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Ensure every user has an associated profile."""
    if created:
        Profile.objects.create(user=instance)
