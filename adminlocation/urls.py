# adminlocation/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeliveryChargeRuleViewSet, LocationViewSet, calculate_delivery_charge

router = DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'delivery-charge-rules', DeliveryChargeRuleViewSet)

urlpatterns = [
   path('delivery-charge/calculate/', calculate_delivery_charge),
   path('', include(router.urls)),
]
