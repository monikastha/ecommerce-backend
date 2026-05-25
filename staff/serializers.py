from rest_framework import serializers
from .models import Staff

class StaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Staff
        fields = ['id', 'user', 'name', 'username', 'email', 'role', 'phone', 'address', 'password']
