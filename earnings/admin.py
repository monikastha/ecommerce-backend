from django.contrib import admin

from .models import CommissionSettings


@admin.register(CommissionSettings)
class CommissionSettingsAdmin(admin.ModelAdmin):
    list_display = ('commission_rate', 'normal_delivery_charge', 'emergency_delivery_charge', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Commission Settings', {
            'fields': ('commission_rate',),
            'description': 'Set the global commission percentage that admin earns from each order',
        }),
        ('Delivery Charges', {
            'fields': ('normal_delivery_charge', 'emergency_delivery_charge'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
