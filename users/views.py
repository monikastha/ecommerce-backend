from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from .models import Users
from .serializers import UsersSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from .utils import generate_otp
from .models import OTP
from django.core.mail import send_mail
from seller.models import Seller
from staff.models import Staff
from deliveryman.models import Deliveryman

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

        response_data = {
            "message": "Login successful",
            "user_id": user.id,
            "username": user.username,
            "name": user.name,
            "email": user.email,
            "profile_image": user.profile_image.url if user.profile_image else None,
            "role": user.role,
        }

        if user.role == "seller":
            try:
                seller = user.seller
            except Seller.DoesNotExist:
                return Response(
                    {"error": "Seller profile not found"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if seller.status != "approved" or not seller.is_approved:
                return Response(
                    {"error": "Your seller account is not approved by admin yet"},
                    status=status.HTTP_403_FORBIDDEN
                )

            response_data["seller_id"] = seller.id
            response_data["seller_status"] = seller.status

        if user.role in ["assistant", "warehousestaff"]:
            try:
                response_data["staff_id"] = user.staff_profile.id
            except Staff.DoesNotExist:
                response_data["staff_id"] = None

        if user.role == "delivery":
            try:
                response_data["delivery_id"] = user.delivery_profile.id
            except Deliveryman.DoesNotExist:
                response_data["delivery_id"] = None

        # Login successful
        return Response(response_data, status=status.HTTP_200_OK)


class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({
                'error': 'Email is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # generate otp
        otp = generate_otp()

        # delete old OTPs
        OTP.objects.filter(email=email).delete()

        # save new OTP
        OTP.objects.create(
            email=email,
            otp=otp
        )

        send_mail(
            subject='Your OTP Code',
            message=f'Your OTP is {otp}',
            from_email=None,
            recipient_list=[email]
        )

        return Response({
            'message': 'OTP sent successfully'
        },status=status.HTTP_200_OK)
    
class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        entered_otp = request.data.get('otp')

        try:
            otp_obj = OTP.objects.get(email=email)
            print(otp_obj)

            # delete that email row if otp expires
            if otp_obj.is_expired():
                otp_obj.delete()

                return Response({
                    'error': 'OTP expired'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if otp_obj.otp == entered_otp:

                otp_obj.delete()

                return Response({
                    'message': 'OTP verified successfully'
                }, status=status.HTTP_200_OK)

            return Response({
                'error': 'Invalid OTP'
            }, status=status.HTTP_400_BAD_REQUEST)
        except OTP.DoesNotExist:
            return Response({
                'error' : "No OTP found"
            }, status=status.HTTP_400_BAD_REQUEST)

            

class UsersViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]
