from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from .models import Users
from .serializers import UsersSerializer
from rest_framework.viewsets import ModelViewSet
from .utils import generate_otp
from .models import OTP
from django.core.mail import send_mail
from seller.models import Seller

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
            "role": user.role,
        }

        if user.role == "seller":
            try:
                response_data["seller_id"] = user.seller.id
            except Seller.DoesNotExist:
                response_data["seller_id"] = None

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
