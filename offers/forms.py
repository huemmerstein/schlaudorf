"""Forms for creating offers."""
from django import forms

from .models import Offer


class OfferForm(forms.ModelForm):
    """Form for users to submit help offers."""

    class Meta:
        model = Offer
        fields = ["title", "description", "latitude", "longitude"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
