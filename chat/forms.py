"""Forms used for sending messages."""
from django import forms


class ChatForm(forms.Form):
    """Form for posting a message in the public chat."""

    content = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Share something with the village...'}),
    )


class DirectMessageForm(forms.Form):
    """Form for sending a private message."""

    recipient = forms.CharField(
        label='Recipient',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    content = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Your message...'}),
    )


class ProfileForm(forms.ModelForm):
    """Allow users to update their profile avatar."""

    class Meta:
        from .models import Profile
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
