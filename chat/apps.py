"""Application configuration for the chat app."""
from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'
    verbose_name = 'Village Chat'

    def ready(self) -> None:  # pragma: no cover - wiring signals
        """Import signal handlers when the app is ready."""
        from . import signals  # noqa: F401
