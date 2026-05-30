from .models import Deliveryman
from rest_framework import serializers
class DeliverymanSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Deliveryman
        fields = ['id', 'user', 'name', 'username', 'email', 'phone', 'address', 'profile_image', 'password']
