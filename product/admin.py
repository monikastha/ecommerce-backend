from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'seller', 'category', 'price', 'quantity', 'status', 'is_published')
    list_filter = ('status', 'is_published', 'category', 'seller')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at')
