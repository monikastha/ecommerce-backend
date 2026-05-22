from .models import Deliveryman
from rest_framework import serializers
class DeliverymanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deliveryman
        fields = '__all__'
