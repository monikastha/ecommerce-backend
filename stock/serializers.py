from rest_framework import serializers
from .models import Stock

class StockSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    product_category = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()
    product_image = serializers.SerializerMethodField()

    class Meta:
        model = Stock
        fields = [
            'id',
            'product',
            'product_name',
            'product_category',
            'category_name',
            'product_price',
            'product_image',
            'quantity',
            'availability_status',
            'available_to_buyers',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_product_name(self, obj):
        return obj.product.name if obj.product else obj.product_name

    def get_product_category(self, obj):
        return obj.product.category_id if obj.product else obj.productcategory_id

    def get_category_name(self, obj):
        if obj.product and obj.product.category:
            return obj.product.category.name
        if obj.productcategory:
            return obj.productcategory.name
        return None

    def get_product_price(self, obj):
        return obj.product.price if obj.product else None

    def get_product_image(self, obj):
        if not obj.product or not obj.product.image:
            return None
        request = self.context.get('request')
        url = obj.product.image.url
        return request.build_absolute_uri(url) if request else url
