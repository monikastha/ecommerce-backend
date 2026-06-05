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
        "age": buyer.age,
        "gender": buyer.gender,
        "phone_number": buyer.phone_number,
        "address": buyer.address,
        "shipping_state": buyer.shipping_state,
        "shipping_city": buyer.shipping_city,
        "shipping_postal_code": buyer.shipping_postal_code,
        "shipping_address": buyer.shipping_address,
        "billing_state": buyer.billing_state,
        "billing_city": buyer.billing_city,
        "billing_postal_code": buyer.billing_postal_code,
        "billing_address": buyer.billing_address,
        "total_orders": buyer.total_orders,
        "total_spent": buyer.total_spent,
        "profile_pic": buyer.profile_pic.url if buyer.profile_pic else None,
        "created_at": buyer.created_at,
        "updated_at": buyer.updated_at,
    }


@api_view(["GET"])
def buyer_list(request):
    buyers = Buyer.objects.select_related("user").all()
    return Response([buyer_payload(buyer) for buyer in buyers], status=status.HTTP_200_OK)


@api_view(["GET", "PATCH", "PUT"])
def buyer_profile(request, user_id):
    try:
        buyer = Buyer.objects.select_related("user").get(user_id=user_id)
    except Buyer.DoesNotExist:
        return Response({
            "error": "Buyer profile not found"
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(buyer_payload(buyer), status=status.HTTP_200_OK)

    data = request.data
    user = buyer.user

    name = data.get("name", buyer.name)
    email = data.get("email", buyer.email)
    username = data.get("username", user.username)

    buyer.name = name
    buyer.email = email
    buyer.phone_number = data.get("phone_number", buyer.phone_number)
    buyer.address = data.get("address", buyer.address)
    buyer.gender = data.get("gender", buyer.gender)
    buyer.shipping_state = data.get("shipping_state", buyer.shipping_state)
    buyer.shipping_city = data.get("shipping_city", buyer.shipping_city)
    buyer.shipping_postal_code = data.get("shipping_postal_code", buyer.shipping_postal_code)
    buyer.shipping_address = data.get("shipping_address", buyer.shipping_address)
    buyer.billing_state = data.get("billing_state", buyer.billing_state)
    buyer.billing_city = data.get("billing_city", buyer.billing_city)
    buyer.billing_postal_code = data.get("billing_postal_code", buyer.billing_postal_code)
    buyer.billing_address = data.get("billing_address", buyer.billing_address)

    age = data.get("age", buyer.age)
    try:
        buyer.age = int(age) if str(age).strip() else None
    except ValueError:
        return Response({
            "error": "Age must be a valid number"
        }, status=status.HTTP_400_BAD_REQUEST)

    user.name = name
    user.email = email
    user.username = username

    try:
        with transaction.atomic():
            user.save()
            buyer.save()
    except IntegrityError:
        return Response({
            "error": "A buyer with this email, username, or phone number already exists"
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response(buyer_payload(buyer), status=status.HTTP_200_OK)


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
