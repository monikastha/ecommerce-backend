app_name = 'earnings'

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommissionSettingsViewSet

router = DefaultRouter()
router.register(r'commission', CommissionSettingsViewSet, basename='commission')

urlpatterns = [
    path('', include(router.urls)),
]
