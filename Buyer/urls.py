from django.urls import path

from .views import buyer_register, buyer_list, buyer_profile

urlpatterns = [
    path("", buyer_list),
    path("register/", buyer_register),
    path("profile/<int:user_id>/", buyer_profile),
]
