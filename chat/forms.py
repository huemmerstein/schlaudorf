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
    """Allow users to update their profile information."""

    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

    class Meta:
        from .models import Profile
        model = Profile
        fields = ['avatar', 'bio', 'address', 'phone']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['bio'].initial = self.instance.bio
            self.fields['address'].initial = self.instance.address
            self.fields['phone'].initial = self.instance.phone

    def save(self, commit=True):
        profile = super().save(commit=False)
        profile.bio = self.cleaned_data.get('bio', '')
        profile.address = self.cleaned_data.get('address', '')
        profile.phone = self.cleaned_data.get('phone', '')
        if commit:
            profile.save()
        return profile
