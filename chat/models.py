"""Database models for the chat features."""
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    """Additional information for each user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"Profile({self.user.username})"


class ChatMessage(models.Model):
    """A message visible to the entire village."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.user.username}: {self.content[:20]}"


class DirectMessage(models.Model):
    """A private message between two users that expires after two days."""

    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"{self.sender.username} → {self.recipient.username}"

    @classmethod
    def prune_old(cls) -> None:
        """Delete direct messages older than two days."""
        threshold = timezone.now() - timedelta(days=2)
        cls.objects.filter(created_at__lt=threshold).delete()
