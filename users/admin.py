from django.contrib import admin
from .models import Users, OTP
class OTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp', 'created_at')
admin.site.register(Users)
admin.site.register(OTP, OTPAdmin)