from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from .models import Users
from .serializers import UsersSerializer
from rest_framework.viewsets import ModelViewSet


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role")

        # Basic validation
        if not username or not password or not role:
            return Response(
                {"error": "Username, password and role are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Use Django's authenticate() - handles hashed passwords correctly
        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if role matches
        if user.role != role:
            return Response(
                {"error": "Role does not match"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Login successful
        return Response({
            "message": "Login successful",
            "username": user.username,
            "role": user.role,
        }, status=status.HTTP_200_OK)


class UsersViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer