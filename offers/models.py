"""Models for neighborhood help offers."""
from django.contrib.auth.models import User
from django.db import models


class Offer(models.Model):
    """A help offer with a location and description."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.title} by {self.user.username}"
