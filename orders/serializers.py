from decimal import Decimal
from uuid import uuid4
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from adminlocation.models import Location
from product.models import Product
from stock.models import Stock
from cart.models import Cart
from deliveryman.serializers import DeliverymanSerializer
from earnings.models import CommissionSettings
from .models import Order, OrderItem

User = get_user_model()


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product',
            'product_name',
            'product_category',
            'product_image',
            'selected_size',
            'quantity',
            'price',
            'subtotal',
            'created_at',
        ]
        read_only_fields = ['created_at']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    assigned_deliveryman_detail = DeliverymanSerializer(source='assigned_deliveryman', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'order_number',
            'user',
            'buyer_username',
            'customer_name',
            'email',
            'phone',
            'address',
            'city',
            'postal_code',
            'delivery_location',
            'delivery_location_name',
            'delivery_type',
            'delivery_fee',
            'payment_type',
            'subtotal',
            'total',
            'commission_rate',
            'status',
            'notes',
            'assigned_deliveryman',
            'assigned_deliveryman_detail',
            'items',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'commission_rate',
            'created_at',
            'updated_at',
        ]


class OrderCreateSerializer(serializers.Serializer):
    order_number = serializers.CharField(required=False, allow_blank=True)
    user_id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False, allow_blank=True)
    customer_name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    address = serializers.CharField()
    city = serializers.CharField()
    postal_code = serializers.CharField()
    delivery_location = serializers.IntegerField(required=False, allow_null=True)
    delivery_location_name = serializers.CharField(required=False, allow_blank=True)
    delivery_type = serializers.ChoiceField(choices=Order.DELIVERY_CHOICES, default='normal')
    delivery_fee = serializers.DecimalField(max_digits=12, decimal_places=2, default=0)
    payment_type = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES, default='cash_on_delivery')
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES, default='pending')
    notes = serializers.CharField(required=False, allow_blank=True)
    reduce_stock = serializers.BooleanField(default=True)
    clear_cart = serializers.BooleanField(default=False)
    items = serializers.ListField(child=serializers.DictField(), min_length=1)

    def _resolve_user(self, data):
        user_id = data.get('user_id')
        username = data.get('username')
        if user_id:
            return User.objects.filter(id=user_id, role='buyer').first()
        if username:
            return User.objects.filter(username=username, role='buyer').first()
        request = self.context.get('request')
        if request and request.user and request.user.is_authenticated:
            return request.user
        return None

    def _product_image(self, product):
        if not product.image:
            return ''
        request = self.context.get('request')
        url = product.image.url
        return request.build_absolute_uri(url) if request else url

    def create(self, validated_data):
        raw_items = validated_data.pop('items')
        reduce_stock = validated_data.pop('reduce_stock', True)
        clear_cart = validated_data.pop('clear_cart', False)
        user = self._resolve_user(validated_data)
        username = validated_data.pop('username', '') or (user.username if user else '')
        validated_data.pop('user_id', None)

        location_id = validated_data.pop('delivery_location', None)
        location = Location.objects.filter(id=location_id).first() if location_id else None
        if location and not validated_data.get('delivery_location_name'):
            validated_data['delivery_location_name'] = f'{location.name}, {location.city}'

        order_number = validated_data.get('order_number') or f'ORD-{uuid4().hex[:8].upper()}'
        validated_data['order_number'] = order_number
        validated_data['user'] = user
        validated_data['buyer_username'] = username
        validated_data['delivery_location'] = location

        prepared_items = []
        subtotal = Decimal('0')

        with transaction.atomic():
            for raw_item in raw_items:
                product_id = raw_item.get('product') or raw_item.get('id')
                try:
                    quantity = int(raw_item.get('quantity') or 1)
                except (TypeError, ValueError) as exc:
                    raise serializers.ValidationError({'items': 'Item quantity must be a number'}) from exc
                if quantity < 1:
                    raise serializers.ValidationError({'items': 'Item quantity must be at least 1'})

                try:
                    product = Product.objects.select_related('category').get(
                        id=product_id,
                        status='approved',
                        is_published=True,
                    )
                except Product.DoesNotExist as exc:
                    raise serializers.ValidationError({'items': f'Product {product_id} is not available'}) from exc

                stock = Stock.objects.select_for_update().filter(product=product, available_to_buyers=True).first()
                if reduce_stock:
                    if not stock or stock.quantity < quantity:
                        raise serializers.ValidationError({'items': f'Out of Stock: {product.name}'})
                    stock.quantity -= quantity
                    stock.availability_status = 'out_of_stock' if stock.quantity <= 0 else 'low_stock' if stock.quantity < 10 else 'in_stock'
                    stock.save(update_fields=['quantity', 'availability_status', 'updated_at'])

                price = Decimal(str(raw_item.get('price') or product.price))
                item_subtotal = price * quantity
                subtotal += item_subtotal
                prepared_items.append({
                    'product': product,
                    'product_name': product.name,
                    'product_category': product.category.name if product.category else '',
                    'product_image': raw_item.get('image') or self._product_image(product),
                    'selected_size': raw_item.get('size') or raw_item.get('selected_size') or '',
                    'quantity': quantity,
                    'price': price,
                    'subtotal': item_subtotal,
                })

            delivery_fee = validated_data.get('delivery_fee') or Decimal('0')
            commission_settings = CommissionSettings.get_settings()
            validated_data['subtotal'] = subtotal
            validated_data['total'] = subtotal + delivery_fee
            validated_data['commission_rate'] = commission_settings.commission_rate
            order = Order.objects.create(**validated_data)
            OrderItem.objects.bulk_create([
                OrderItem(order=order, **item) for item in prepared_items
            ])

            if clear_cart and user:
                Cart.objects.filter(user=user).delete()
            elif clear_cart and username:
                Cart.objects.filter(user=None, buyer_username=username).delete()

        return order
