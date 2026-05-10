from rest_framework import serializers
from .models import AdminPerson

class AdminPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminPerson
        fields = '__all__'