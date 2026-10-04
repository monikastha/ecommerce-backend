from django.urls import path
from .views import send_test_notification

urlpatterns = [
    path('test-send/', send_test_notification),
]
