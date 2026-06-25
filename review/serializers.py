from rest_framework import serializers
from django.utils import timezone
from orders.models import OrderItem
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_seller = serializers.IntegerField(source='product.seller_id', read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = [
            'sentiment',
            'seller_reply_message',
            'seller_reply_name',
            'seller_reply_at',
            'date',
            'created_at',
            'updated_at',
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs.get('parent'):
            return attrs

        product = attrs.get('product')
        buyer_username = attrs.get('buyer_username') or ''
        request = self.context.get('request')
        user = request.user if request and request.user and request.user.is_authenticated else None
        if not buyer_username and user:
            buyer_username = user.username
            attrs['buyer_username'] = buyer_username

        if not product:
            raise serializers.ValidationError({'product': 'Product is required for reviews.'})

        purchased = OrderItem.objects.filter(
            product=product,
            order__status__in=[
                'pending',
                'seller_accepted',
                'preparing',
                'warehouse_processing',
                'ready_for_delivery',
                'delivery_assigned',
                'delivery_accepted',
                'picked_up',
                'out_for_delivery',
                'delivered',
                'confirmed',
                'processing',
                'shipped',
            ],
        )
        if user:
            purchased = purchased.filter(order__user=user)
        elif buyer_username:
            purchased = purchased.filter(order__buyer_username=buyer_username)
        else:
            raise serializers.ValidationError({'buyer_username': 'Buyer username is required.'})

        if not purchased.exists():
            raise serializers.ValidationError('You can review this product only after purchasing it.')

        return attrs


class ReviewReplySerializer(serializers.Serializer):
    message = serializers.CharField(trim_whitespace=True)
    seller_name = serializers.CharField(required=False, allow_blank=True, trim_whitespace=True)

    def save(self, review):
        review.seller_reply_message = self.validated_data['message']
        review.seller_reply_name = self.validated_data.get('seller_name') or 'Seller'
        review.seller_reply_at = timezone.now()
        review.save(update_fields=['seller_reply_message', 'seller_reply_name', 'seller_reply_at', 'updated_at'])
        return review
