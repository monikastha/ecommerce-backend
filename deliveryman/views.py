from rest_framework import viewsets, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from django.db import transaction
from .models import Deliveryman
from .serializers import DeliverymanSerializer
from users.models import Users


class DeliverymanViewSet(viewsets.ModelViewSet):
    queryset = Deliveryman.objects.all().order_by('-id')
    serializer_class = DeliverymanSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        password = data.pop('password', None)
        if isinstance(password, list):
            password = password[0] if password else None

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                deliveryman = serializer.save()
                if deliveryman.user:
                    deliveryman.user.name = deliveryman.name
                    deliveryman.user.username = deliveryman.username
                    deliveryman.user.email = deliveryman.email
                    deliveryman.user.role = 'delivery'
                    if password:
                        deliveryman.user.set_password(password)
                    deliveryman.user.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data

        user_data = {
            'username': data.get('username'),
            'email': data.get('email'),
            'name': data.get('name'),
            'role': 'delivery',
            'password': data.get('password')
        }

        # Basic Validation
        if not user_data['username'] or not user_data['email'] or not user_data['name'] or not user_data['password']:
            return Response({
                "error": "Username, email, name and password are required"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check for duplicates
        if Users.objects.filter(username=user_data['username']).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        if Users.objects.filter(email=user_data['email']).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # 1. Create User (with hashed password)
                user = Users.objects.create(
                    username=user_data['username'],
                    email=user_data['email'],
                    name=user_data['name'],
                    role='delivery',
                    is_verified=True
                )
                user.set_password(user_data['password'])   # ← This is crucial
                user.save()

                # 2. Create Deliveryman Profile linked to User
                deliveryman = Deliveryman.objects.create(
                    user=user,
                    name=user_data['name'],
                    username=user_data['username'],
                    email=user_data['email'],
                    phone=data.get('phone'),
                    address=data.get('address'),
                )

                serializer = self.get_serializer(deliveryman)

                return Response({
                    "message": "Deliveryman created successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "role": user.role
                    },
                    "deliveryman": serializer.data
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
