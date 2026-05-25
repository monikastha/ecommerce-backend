from django.db import IntegrityError, transaction
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status

from users.models import OTP, Users
from .models import Seller


def seller_payload(seller):
    return {
        'id': seller.id,
        'name': seller.user.name,
        'username': seller.user.username,
        'email': seller.user.email,
        'phone': seller.phone,
        'citizenship': seller.citizenship,
        'pan_no': seller.pan_no,
        'address': seller.address,
        'status': seller.status,
        'is_approved': seller.is_approved,
        'logo': seller.logo.url if seller.logo else None,
        'business_certificate': (
            seller.business_certificate.url
            if seller.business_certificate
            else None
        ),
        'created_at': seller.user.created_at,
    }


def validate_otp(email, entered_otp):
    if not email:
        return 'Email is required'

    if not entered_otp:
        return 'OTP is required'

    try:
        otp_obj = OTP.objects.get(email=email)
    except OTP.DoesNotExist:
        return 'No OTP found for this email'

    if otp_obj.is_expired():
        otp_obj.delete()
        return 'OTP expired'

    if otp_obj.otp != entered_otp:
        return 'Invalid OTP'

    otp_obj.delete()
    return None


@api_view(['GET'])
def seller_list(request):
    sellers = Seller.objects.select_related('user').order_by('-id')
    return Response([seller_payload(seller) for seller in sellers])


@api_view(['GET', 'PUT', 'PATCH'])
@parser_classes([MultiPartParser, FormParser])
def seller_detail(request, seller_id):
    try:
        seller = Seller.objects.select_related('user').get(id=seller_id)
    except Seller.DoesNotExist:
        return Response({'error': 'Seller not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(seller_payload(seller))

    data = request.data
    user = seller.user

    user.name = data.get('name', user.name)
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    if data.get('password'):
        user.set_password(data.get('password'))
    user.save()

    seller.phone = data.get('phone', seller.phone)
    seller.citizenship = data.get('citizenship', seller.citizenship)
    seller.pan_no = data.get('pan_no', seller.pan_no)
    seller.address = data.get('address', seller.address)
    if data.get('status') in ['pending', 'approved', 'rejected']:
        seller.status = data.get('status')
        seller.is_approved = seller.status == 'approved'
    if request.FILES.get('logo'):
        seller.logo = request.FILES['logo']
    if request.FILES.get('business_certificate'):
        seller.business_certificate = request.FILES['business_certificate']
    seller.save()

    return Response({
        'message': 'Seller updated successfully',
        'seller': seller_payload(seller),
    })


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def seller_register(request):
    data = request.data
    required_fields = [
        'name',
        'username',
        'email',
        'phone',
        'password',
        'confirm_password',
        'citizenship',
        'pan_no',
        'address',
        'otp',
    ]

    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return Response({
            'error': f"Missing required fields: {', '.join(missing_fields)}"
        }, status=status.HTTP_400_BAD_REQUEST)

    if data.get('password') != data.get('confirm_password'):
        return Response({
            'error': 'Passwords do not match'
        }, status=status.HTTP_400_BAD_REQUEST)

    if 'logo' not in request.FILES:
        return Response({
            'error': 'Shop logo is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    if 'business_certificate' not in request.FILES:
        return Response({
            'error': 'Registration document is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    otp_error = validate_otp(data.get('email'), data.get('otp'))
    if otp_error:
        return Response({'error': otp_error}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            user = Users(
                name=data.get('name'),
                username=data.get('username'),
                email=data.get('email'),
                role='seller',
                is_verified=True,
            )
            user.set_password(data.get('password'))
            user.save()

            seller = Seller.objects.create(
                user=user,
                phone=data.get('phone'),
                citizenship=data.get('citizenship'),
                pan_no=data.get('pan_no'),
                address=data.get('address'),
                logo=request.FILES['logo'],
                business_certificate=request.FILES['business_certificate'],
            )
    except IntegrityError:
        return Response({
            'error': 'A user with this email or username already exists'
        }, status=status.HTTP_400_BAD_REQUEST)

    return Response({
        'message': 'Seller registered successfully',
        'seller': seller_payload(seller),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def approve_seller(request, seller_id):
    try:
        seller = Seller.objects.get(id=seller_id)
    except Seller.DoesNotExist:
        return Response({'error': 'Seller not found'}, status=status.HTTP_404_NOT_FOUND)

    seller.status = 'approved'
    seller.is_approved = True
    seller.save(update_fields=['status', 'is_approved'])

    return Response({
        'message': 'Seller approved successfully',
        'seller': seller_payload(seller),
    })


@api_view(['POST'])
def reject_seller(request, seller_id):
    try:
        seller = Seller.objects.get(id=seller_id)
    except Seller.DoesNotExist:
        return Response({'error': 'Seller not found'}, status=status.HTTP_404_NOT_FOUND)

    seller.status = 'rejected'
    seller.is_approved = False
    seller.save(update_fields=['status', 'is_approved'])

    return Response({
        'message': 'Seller rejected successfully',
        'seller': seller_payload(seller),
    })

