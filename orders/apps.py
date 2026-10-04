from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'
    def ready(self):
        # import signal handlers
        try:
            from . import signals  # noqa: F401
        except Exception:
            pass
