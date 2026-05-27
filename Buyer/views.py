from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import Users
from .models import Buyer


def buyer_payload(buyer):
    return {
        "id": buyer.id,
        "user_id": buyer.user_id,
        "name": buyer.name,
        "username": buyer.user.username,
        "email": buyer.email,
        "phone_number": buyer.phone_number,
        "address": buyer.address,
        "role": buyer.user.role,
    }


@api_view(["POST"])
def buyer_register(request):
    data = request.data
    required_fields = [
        "username",
        "fullName",
        "email",
        "phoneNumber",
        "address",
        "password",
        "confirmPassword",
    ]

    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return Response({
            "error": f"Missing required fields: {', '.join(missing_fields)}"
        }, status=status.HTTP_400_BAD_REQUEST)

    if data.get("password") != data.get("confirmPassword"):
        return Response({
            "error": "Passwords do not match"
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            user = Users(
                name=data.get("fullName"),
                username=data.get("username"),
                email=data.get("email"),
                role="buyer",
                is_verified=True,
            )
            user.set_password(data.get("password"))
            user.save()

            buyer = Buyer.objects.create(
                user=user,
                name=data.get("fullName"),
                email=data.get("email"),
                phone_number=data.get("phoneNumber"),
                address=data.get("address"),
                shipping_address=data.get("address"),
            )
    except IntegrityError:
        return Response({
            "error": "A buyer with this email, username, or phone number already exists"
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        "message": "Buyer registered successfully",
        "buyer": buyer_payload(buyer),
    }, status=status.HTTP_201_CREATED)
