from django.conf import settings
from django.db import models

from help_requests.models import HelpRequest


class Appointment(models.Model):
    STATUS = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("done", "Done"),
    ]

    help_request = models.ForeignKey(HelpRequest, on_delete=models.CASCADE)
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="requested_appointments", on_delete=models.CASCADE
    )
    helper = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="accepted_appointments", on_delete=models.CASCADE
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    notes = models.TextField(blank=True)
