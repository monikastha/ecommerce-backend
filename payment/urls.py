app_name = 'payment'

from django.urls import path
from .views import initiate_esewa, initiate_khalti, record_cod_payment

urlpatterns = [
    path('initiate-esewa/', initiate_esewa, name='initiate-esewa'),
    path('initiate-khalti/', initiate_khalti, name='initiate-khalti'),
    path('record-cod-payment/', record_cod_payment, name='record-cod-payment'),
]
