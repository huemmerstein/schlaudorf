"""Database models for the chat features."""
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
from cryptography.fernet import Fernet

fernet = Fernet(settings.FERNET_KEY)


class Profile(models.Model):
    """Additional information for each user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio_encrypted = models.TextField(blank=True, default='')
    address_encrypted = models.TextField(blank=True, default='')
    phone_encrypted = models.CharField(max_length=255, blank=True, default='')
    is_approved = models.BooleanField(default=False)

    def _encrypt(self, value: str) -> str:
        return fernet.encrypt(value.encode()).decode() if value else ''

    def _decrypt(self, value: str) -> str:
        if not value:
            return ''
        try:
            return fernet.decrypt(value.encode()).decode()
        except Exception:  # pragma: no cover - decryption error
            return ''

    @property
    def bio(self) -> str:
        return self._decrypt(self.bio_encrypted)

    @bio.setter
    def bio(self, value: str) -> None:
        self.bio_encrypted = self._encrypt(value)

    @property
    def address(self) -> str:
        return self._decrypt(self.address_encrypted)

    @address.setter
    def address(self, value: str) -> None:
        self.address_encrypted = self._encrypt(value)

    @property
    def phone(self) -> str:
        return self._decrypt(self.phone_encrypted)

    @phone.setter
    def phone(self, value: str) -> None:
        self.phone_encrypted = self._encrypt(value)

    def __str__(self) -> str:  # pragma: no cover - simple representation
        return f"Profile({self.user.username})"


class ChatMessage(models.Model):
    """A message visible to the entire village."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    offer = models.ForeignKey('offers.Offer', null=True, blank=True, on_delete=models.SET_NULL)
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

    def save(self, *args, **kwargs):
        if self.content and not self.content.startswith('gAAAA'):
            self.content = fernet.encrypt(self.content.encode()).decode()
        super().save(*args, **kwargs)

    @property
    def content_plain(self) -> str:
        try:
            return fernet.decrypt(self.content.encode()).decode()
        except Exception:  # pragma: no cover - decryption error
            return ''

    @classmethod
    def prune_old(cls) -> None:
        """Delete direct messages older than two days."""
        threshold = timezone.now() - timedelta(days=2)
        cls.objects.filter(created_at__lt=threshold).delete()
