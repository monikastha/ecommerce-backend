# import random
# from datetime import timedelta

# from django.utils import timezone
# from django.core.mail import send_mail
# from django.conf import settings

# from .models import OTP


# def generate_otp() -> str:
#     """Generate a 6-digit OTP"""
#     return str(random.randint(100000, 999999))


# def send_otp_email(email: str, role: str = None) -> bool:
#     """
#     Send OTP to user's email and save it in database
#     """
#     # Remove previous OTPs for this email
#     OTP.objects.filter(email=email).delete()

#     otp_code = generate_otp()
#     expires_at = timezone.now() + timedelta(minutes=10)

#     # Save OTP in database
#     OTP.objects.create(
#         email=email,
#         code=otp_code,
#         role=role,
#         expires_at=expires_at
#     )

#     subject = "Sajilo Mart - Your Verification Code"
    
#     message = f"""
#     Dear User,

#     Your One-Time Password (OTP) for Sajilo Mart is: **{otp_code}**

#     This code will expire in 10 minutes.

#     If you did not request this OTP, please ignore this email.

#     Thank you for choosing Sajilo Mart!
    
#     Regards,
#     Sajilo Mart Team 🇳🇵
#     """

#     try:
#         send_mail(
#             subject=subject,
#             message=message,
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[email],
#             fail_silently=False,
#         )
#         print(f"OTP sent successfully to {email}")
#         return True

#     except Exception as e:
#         print(f"Failed to send OTP email: {e}")
#         return False