from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with simple role flags."""

    is_helper = models.BooleanField(default=False)
    is_requester = models.BooleanField(default=True)
