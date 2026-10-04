from django.urls import re_path
from .consumers import AssistantNotificationConsumer

websocket_urlpatterns = [
    re_path(r"ws/notifications/assistant/$", AssistantNotificationConsumer.as_asgi()),
]
