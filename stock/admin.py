from django.contrib import admin
from .models import Stock

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'quantity', 'availability_status', 'created_at']
    list_filter = ['availability_status']
    search_fields = ['product_name']