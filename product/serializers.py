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
            'size',
            'image',
            'status',
            'is_published',
            'rejection_reason',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        category = attrs.get('category') or getattr(self.instance, 'category', None)
        size = attrs.get('size')
        if size is None and self.instance is not None:
            size = self.instance.size

        if category and category.requires_size and not str(size or '').strip():
            raise serializers.ValidationError({
                'size': 'Size is required for this category.'
            })

        if size is not None:
            attrs['size'] = str(size).strip()

        return attrs
