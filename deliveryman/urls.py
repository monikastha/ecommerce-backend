from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeliverymanViewSet

router = DefaultRouter()
router.register(r"delivery", DeliverymanViewSet,basename="deliveryman")

urlpatterns = [
    path("", include(router.urls)),
]