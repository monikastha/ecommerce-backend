from django.urls import path
from .views import approve_seller, reject_seller, seller_list, seller_register

urlpatterns = [
    path('', seller_list),
    path('register/', seller_register),
    path('<int:seller_id>/approve/', approve_seller),
    path('<int:seller_id>/reject/', reject_seller),
]
