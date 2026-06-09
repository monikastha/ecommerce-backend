from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response

from Buyer.models import Buyer
from deliveryman.models import Deliveryman
from seller.models import Seller
from staff.models import Staff
from users.models import Users

from .serializers import ProfileSerializer


def image_url(file_field):
    return file_field.url if file_field else None


def profile_for_user(user):
    role = user.role
    if role == "buyer":
        return Buyer.objects.filter(user=user).first()
    if role == "seller":
        return Seller.objects.filter(user=user).first()
    if role == "delivery":
        return Deliveryman.objects.filter(user=user).first()
    if role in ["assistant", "warehousestaff"]:
        return Staff.objects.filter(user=user).first()
    return getattr(user, "admin_person", None)


def profile_payload(user):
    profile = profile_for_user(user)
    payload = {
        "id": user.id,
        "user_id": user.id,
        "profile_id": profile.id if profile else None,
        "role": user.role,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "profile_image": image_url(user.profile_image),
    }

    if user.role == "buyer" and profile:
        payload.update({
            "id": profile.id,
            "user_id": user.id,
            "phone_number": profile.phone_number,
            "phone": profile.phone_number,
            "address": profile.address,
            "age": profile.age,
            "gender": profile.gender,
            "shipping_state": profile.shipping_state,
            "shipping_city": profile.shipping_city,
            "shipping_postal_code": profile.shipping_postal_code,
            "shipping_address": profile.shipping_address,
            "billing_state": profile.billing_state,
            "billing_city": profile.billing_city,
            "billing_postal_code": profile.billing_postal_code,
            "billing_address": profile.billing_address,
            "total_orders": profile.total_orders,
            "total_spent": profile.total_spent,
            "profile_image": image_url(profile.profile_pic) or image_url(user.profile_image),
            "profile_pic": image_url(profile.profile_pic),
            "created_at": profile.created_at,
            "updated_at": profile.updated_at,
        })

    if user.role == "seller" and profile:
        payload.update({
            "id": profile.id,
            "profile_id": profile.id,
            "phone": profile.phone,
            "address": profile.address,
            "citizenship": profile.citizenship,
            "pan_no": profile.pan_no,
            "status": profile.status,
            "is_approved": profile.is_approved,
            "profile_image": image_url(profile.logo) or image_url(user.profile_image),
            "logo": image_url(profile.logo),
        })

    if user.role in ["assistant", "warehousestaff"] and profile:
        payload.update({
            "id": profile.id,
            "profile_id": profile.id,
            "phone": profile.phone,
            "address": profile.address,
            "profile_image": image_url(profile.profile_image) or image_url(user.profile_image),
        })

    if user.role == "delivery" and profile:
        payload.update({
            "id": profile.id,
            "profile_id": profile.id,
            "phone": profile.phone,
            "address": profile.address,
            "profile_image": image_url(profile.profile_image) or image_url(user.profile_image),
        })

    return payload


def set_if_present(instance, data, field, target_field=None):
    if field in data:
        setattr(instance, target_field or field, data.get(field))


@api_view(["GET", "PATCH", "PUT"])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def user_profile(request, user_id):
    try:
        user = Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        return Response(profile_payload(user), status=status.HTTP_200_OK)

    serializer = ProfileSerializer(data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    profile = profile_for_user(user)

    try:
        with transaction.atomic():
            set_if_present(user, data, "name")
            set_if_present(user, data, "username")
            set_if_present(user, data, "email")
            if data.get("password"):
                user.set_password(data["password"])
            if request.FILES.get("profile_image"):
                user.profile_image = request.FILES["profile_image"]
            user.save()

            if user.role == "buyer" and profile:
                set_if_present(profile, data, "name")
                set_if_present(profile, data, "email")
                set_if_present(profile, data, "phone_number")
                if "phone" in data and "phone_number" not in data:
                    profile.phone_number = data.get("phone")
                for field in [
                    "address",
                    "age",
                    "gender",
                    "shipping_state",
                    "shipping_city",
                    "shipping_postal_code",
                    "shipping_address",
                    "billing_state",
                    "billing_city",
                    "billing_postal_code",
                    "billing_address",
                ]:
                    set_if_present(profile, data, field)
                if request.FILES.get("profile_image"):
                    profile.profile_pic = request.FILES["profile_image"]
                profile.save()

            if user.role == "seller" and profile:
                set_if_present(profile, data, "phone")
                set_if_present(profile, data, "address")
                if request.FILES.get("profile_image"):
                    profile.logo = request.FILES["profile_image"]
                if request.FILES.get("logo"):
                    profile.logo = request.FILES["logo"]
                profile.save()

            if user.role in ["assistant", "warehousestaff"] and profile:
                set_if_present(profile, data, "name")
                set_if_present(profile, data, "username")
                set_if_present(profile, data, "email")
                set_if_present(profile, data, "phone")
                set_if_present(profile, data, "address")
                profile.role = user.role
                if request.FILES.get("profile_image"):
                    profile.profile_image = request.FILES["profile_image"]
                profile.save()

            if user.role == "delivery" and profile:
                set_if_present(profile, data, "name")
                set_if_present(profile, data, "username")
                set_if_present(profile, data, "email")
                set_if_present(profile, data, "phone")
                set_if_present(profile, data, "address")
                if request.FILES.get("profile_image"):
                    profile.profile_image = request.FILES["profile_image"]
                profile.save()

    except IntegrityError:
        return Response(
            {"error": "A profile with this username, email, or phone already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(profile_payload(user), status=status.HTTP_200_OK)
