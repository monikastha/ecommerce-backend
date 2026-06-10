from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "username", "email", "role", "is_verified", "updated_at")
    list_filter = ("role", "is_verified")
    search_fields = ("name", "username", "email")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-updated_at",)
