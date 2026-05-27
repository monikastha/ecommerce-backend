from django.urls import path

from .views import buyer_register

urlpatterns = [
    path("register/", buyer_register),
]
