from django.conf import settings
from django.db import models


class HelpRequest(models.Model):
    """A request for help within the community."""

    REQUEST_TYPES = [
        ("shopping", "Shopping"),
        ("repair", "Repair"),
        ("childcare", "Childcare"),
    ]

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    details = models.TextField()
    kind = models.CharField(max_length=20, choices=REQUEST_TYPES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    fulfilled = models.BooleanField(default=False)
