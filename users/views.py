from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .models import Users
from .serializers import UsersSerializer


class LoginView(APIView):

    def post(self, request):   # ✅ FIX GET → POST

        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role")

        try:
            user = Users.objects.get(
                username=username,
                password=password,
                role=role
            )

            return Response({
                "message": "Login successful",
                "username": user.username,
                "role": user.role,
            })

        except Users.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )


class UsersViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer