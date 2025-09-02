from django.contrib import admin

from .models import HelpRequest


@admin.register(HelpRequest)
class HelpRequestAdmin(admin.ModelAdmin):
    list_display = ("title", "requester", "kind", "fulfilled")
    list_filter = ("kind", "fulfilled")
