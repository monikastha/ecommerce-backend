from django.urls import path
from .views import (
    AdminPersonListCreateView,
    AdminPersonDetailView,
    AdminPersonMeView
)

urlpatterns = [
    path('', AdminPersonListCreateView.as_view(), name='adminperson-list-create'),
    path('<int:pk>/', AdminPersonDetailView.as_view(), name='adminperson-detail'),
    path('me/', AdminPersonMeView.as_view(), name='adminperson-me'),   # Current admin's profile
]