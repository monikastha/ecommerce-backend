from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_name = serializers.CharField(source='seller.user.name', read_only=True)
    seller_email = serializers.CharField(source='seller.user.email', read_only=True)

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
            'status',
            'is_published',
            'rejection_reason',
            'created_at',
            'updated_at',
        ]
