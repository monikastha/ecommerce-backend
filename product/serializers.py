from rest_framework import serializers
from .models import Product, ProductImage, ProductColor


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            'id',
            'product',
            'image',
            'image_type',
            'view_number',
            'is_primary',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = [
            'id',
            'product',
            'color_name',
            'color_code',
            'quantity',
            'price_adjustment',
            'is_available',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_name = serializers.CharField(source='seller.user.name', read_only=True)
    seller_email = serializers.CharField(source='seller.user.email', read_only=True)
    product_images = ProductImageSerializer(many=True, read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'seller',
            'seller_name',
            'seller_email',
            'name',
            'category',
            'category_name',
            'code',
            'description',
            'price',
            'quantity',
            'image',
            'product_images',
            'colors',
            'status',
            'is_published',
            'rejection_reason',
            'created_at',
            'updated_at',
        ]
