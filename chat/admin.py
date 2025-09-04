"""Admin configuration for chat models."""
from django.contrib import admin

from .models import ChatMessage, DirectMessage, Profile

admin.site.register(ChatMessage)
admin.site.register(DirectMessage)
admin.site.register(Profile)
