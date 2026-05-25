from rest_framework import viewsets, status
from .models import Staff
from .serializers import StaffSerializer
from rest_framework.response import Response
from users.models import Users
from django.db import transaction


class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all().order_by('-id')
    serializer_class = StaffSerializer

    # VALID ROLES
    VALID_ROLES = ['warehousestaff', 'assistant']

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
                staff = serializer.save()
                if staff.user:
                    staff.user.name = staff.name
                    staff.user.username = staff.username
                    staff.user.email = staff.email
                    staff.user.role = staff.role
                    if password:
                        staff.user.set_password(password)
                    staff.user.save()
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data)

    # CUSTOM CREATE LOGIC
    def create(self, request, *args, **kwargs):
        print("Custom Registration of Staff Triggered")

        # Catch the request data
        data = request.data

        print(data, 'user_data')
        # Create user
        user_data = {
            'username': data.get('username'),
            'email': data.get('email'),
            'name': data.get('name'),
            'address': data.get('address'),
            'role': data.get('role'),
            'phone' : data.get('phone'),
            'password': data.get('password')
        }

        #  staff_data = {}

        # Basic validation
        if not user_data['username'] or not user_data['email'] or not user_data['name']:
            return Response({
                "error": "Username, email or name is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check whether valid role is in request or not
        if user_data['role'] not in self.VALID_ROLES:
            return Response({
                "error": f"Invalid role. Valid roles are: {self.VALID_ROLES}"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check whether email exists already or not
        isEmailAlreadyExists = Users.objects.filter(
            email=user_data['email']).exists()
        if isEmailAlreadyExists:
            return Response({
                "error": "Email already exists"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check whether username exists already or not
        isUsernameAlreadyExists = Users.objects.filter(
            username=user_data['username']).exists()
        if isUsernameAlreadyExists:
            return Response({
                "error": "Username already exists"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():          # ← Transaction Applied Here
                # Create User
                user = Users.objects.create(
                    username=user_data['username'],
                    email=user_data['email'],
                    name=user_data['name'],
                    role=user_data['role'],
                    is_verified=True
                )
                user.set_password(user_data['password'])
                user.save()

                # Create Staff
                staff = Staff.objects.create(
                    user=user,                       # Important: Link User to Staff
                    name=user_data['name'],
                    username=user_data['username'],
                    email=user_data['email'],
                    role=user_data['role'],
                    phone=user_data['phone'],
                    address=user_data['address'],
                )

                # Serialize staff for response
                serializer = self.get_serializer(staff)

                return Response({
                    "message": "Staff created successfully",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email
                    },
                    "staff": serializer.data
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                "error": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
