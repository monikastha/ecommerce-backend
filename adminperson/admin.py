from django.contrib import admin
from .models import AdminPerson


@admin.register(AdminPerson)
class AdminPersonAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'get_username', 'get_email', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'user__name', 'user__email']
    ordering = ['-created_at']

    readonly_fields = ['created_at', 'updated_at']
    fields = ['user', ('created_at', 'updated_at')]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user__role='admin')

    def get_full_name(self, obj):
        return obj.user.name if obj.user else "—"
    get_full_name.short_description = 'Full Name'

    def get_username(self, obj):
        return obj.user.username if obj.user else "—"
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email if obj.user else "—"
    get_email.short_description = 'Email'