# adminlocation/serializers.py
from rest_framework import serializers
from .models import DeliveryChargeRule, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields =  '__all__'


class DeliveryChargeRuleSerializer(serializers.ModelSerializer):
    location_name = serializers.CharField(source='location.name', read_only=True)
    province = serializers.CharField(source='location.province', read_only=True)
    city = serializers.CharField(source='location.city', read_only=True)

    class Meta:
        model = DeliveryChargeRule
        fields = '__all__'
