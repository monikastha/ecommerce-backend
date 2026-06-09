from django.contrib import admin
from .models import Product, ProductImage, ProductColor


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'image_type', 'view_number', 'is_primary')


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1
    fields = ('color_name', 'color_code', 'quantity', 'price_adjustment', 'is_available')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'seller', 'category', 'price', 'quantity', 'status', 'is_published')
    list_filter = ('status', 'is_published', 'category', 'seller')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductImageInline, ProductColorInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image_type', 'view_number', 'is_primary')
    list_filter = ('image_type', 'is_primary')
    search_fields = ('product__name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'color_name', 'color_code', 'quantity', 'is_available')
    list_filter = ('is_available', 'product')
    search_fields = ('product__name', 'color_name')
    readonly_fields = ('created_at', 'updated_at')