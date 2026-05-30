from django.urls import path

from .views import buyer_register, buyer_list

urlpatterns = [
    path("", buyer_list),
    path("register/", buyer_register),
]
