from rest_framework import serializers
from .models import AdminPerson
from django.contrib.auth import get_user_model

User = get_user_model()


class AdminPersonSerializer(serializers.ModelSerializer):
    # Read-only user fields
    user_name = serializers.CharField(source='user.name', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = AdminPerson
        fields = [
            'id',
            'user',
            'user_name',
            'username',
            'email',
            'role',
            'phone',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']


class AdminPersonCreateSerializer(serializers.ModelSerializer):
    """Use this serializer when creating a new AdminPerson"""
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = AdminPerson
        fields = ['username', 'email', 'name', 'password']

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        name = validated_data.pop('name')
        password = validated_data.pop('password')

        # Create User with role = admin
        user = User.objects.create_user(
            username=username,
            email=email,
            name=name,
            role='admin',
            password=password
        )

        admin_person = AdminPerson.objects.create(
            user=user,
        )
        return admin_person