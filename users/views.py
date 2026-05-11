from django.contrib.auth import authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .models import Users
from .serializers import UsersSerializer


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role")

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.role != role:
                return Response(
                    {"error": "Role mismatch"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response({
                "message": "Login successful",
                "username": user.username,
                "role": user.role,
            })

        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_400_BAD_REQUEST
        )


class UsersViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer