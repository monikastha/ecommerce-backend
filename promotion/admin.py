# promotions/admin.py
from django.contrib import admin
from .models import Promotion


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'd_type',
        'discount_display',
        'applies_to',
        'status',
        'start_date',
        'end_date',
    ]
    
    list_filter = ['status', 'd_type', 'applies_to']
    search_fields = ['name']
    
    # Only categories (since products field is not used)
    filter_horizontal = ['categories']
    
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ("Basic Information", {
            'fields': ('name', 'd_type', 'd_value', 'applies_to')
        }),
        ("Target Categories", {
            'fields': ('categories',),
            'description': 'Select one or more categories when "Specific Categories" is chosen.'
        }),
        ("Promotion Duration", {
            'fields': ('start_date', 'end_date')
        }),
        ("Status", {
            'fields': ('status',)
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def discount_display(self, obj):
        """Nice discount display in list view"""
        if obj.d_type == 'percentage' and obj.d_value:
            return f"{obj.d_value}% Off"
        elif obj.d_type == 'fixed' and obj.d_value:
            return f"₹{obj.d_value} Off"
        return "-"
    
    discount_display.short_description = 'Discount'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('categories')