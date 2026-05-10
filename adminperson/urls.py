from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminPersonViewSet

router = DefaultRouter()
router.register(r'adminperson', AdminPersonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]