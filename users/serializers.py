from rest_framework import serializers
from .models import Users
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    role = serializers.CharField()
class UsersSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = [
            "id",
            "username",
            "email",
            "phone",
            "role",
            "password",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = Users(**validated_data)
        user.set_password(password)
        user.save()
        return user
# serializers.py