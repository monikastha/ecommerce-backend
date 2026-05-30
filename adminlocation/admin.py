from django.contrib import admin
from .models import DeliveryChargeRule, Location

admin.site.register(Location)


@admin.register(DeliveryChargeRule)
class DeliveryChargeRuleAdmin(admin.ModelAdmin):
    list_display = (
        'location',
        'delivery_type',
        'min_product_total',
        'max_product_total',
        'charge',
        'status',
    )
    list_filter = ('delivery_type', 'status', 'location__province', 'location__city')
    search_fields = ('location__name', 'location__province', 'location__city')
