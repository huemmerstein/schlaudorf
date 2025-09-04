"""Admin configuration for chat models."""
from django.contrib import admin

from .models import ChatMessage, DirectMessage, Profile

admin.site.register(ChatMessage)
admin.site.register(DirectMessage)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "is_approved")
    list_filter = ("is_approved",)
