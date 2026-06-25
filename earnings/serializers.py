from rest_framework import serializers

from .models import CommissionSettings


class CommissionSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionSettings
        fields = [
            'id',
            'commission_rate',
            'normal_delivery_charge',
            'emergency_delivery_charge',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
