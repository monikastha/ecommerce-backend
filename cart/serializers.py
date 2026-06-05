from rest_framework import serializers
from stock.models import Stock
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_category = serializers.CharField(source='product.category.name', read_only=True)
    product_image = serializers.SerializerMethodField()
    available_stock = serializers.SerializerMethodField()
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_category',
            'product_image',
            'quantity',
            'price_snapshot',
            'available_stock',
            'location',
            'location_name',
            'subtotal',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_product_image(self, obj):
        if not obj.product.image:
            return None
        request = self.context.get('request')
        url = obj.product.image.url
        return request.build_absolute_uri(url) if request else url

    def get_available_stock(self, obj):
        stock = Stock.objects.filter(product=obj.product, available_to_buyers=True).first()
        return stock.quantity if stock else 0


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    item_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'buyer_username',
            'items',
            'total',
            'item_count',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']
