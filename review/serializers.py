from rest_framework import serializers
from django.utils import timezone
from seller.models import Seller
from orders.models import OrderItem
from .models import Review

REVIEWABLE_ORDER_STATUSES = ['delivered']


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

        delivered_purchase = OrderItem.objects.filter(
            product=product,
            order__status__in=REVIEWABLE_ORDER_STATUSES,
        )
        if user:
            delivered_purchase = delivered_purchase.filter(order__user=user)
        elif buyer_username:
            delivered_purchase = delivered_purchase.filter(order__buyer_username=buyer_username)
        else:
            raise serializers.ValidationError({'buyer_username': 'Buyer username is required.'})

        if not delivered_purchase.exists():
            raise serializers.ValidationError('You can review this product only after it has been delivered.')

        return attrs


class ReviewReplySerializer(serializers.Serializer):
    message = serializers.CharField(trim_whitespace=True)
    seller_name = serializers.CharField(required=False, allow_blank=True, trim_whitespace=True)
    seller_id = serializers.IntegerField(required=False)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        review = self.context.get('review')
        request = self.context.get('request')

        if not review or not review.product or not review.product.seller_id:
            raise serializers.ValidationError('This review is not linked to a seller product.')

        seller = None
        user = request.user if request and request.user and request.user.is_authenticated else None
        if user and getattr(user, 'role', None) == 'seller':
            seller = Seller.objects.filter(user=user).first()
        elif attrs.get('seller_id'):
            seller = Seller.objects.filter(id=attrs['seller_id']).first()

        if not seller:
            raise serializers.ValidationError({'seller_id': 'Seller id is required to reply to this review.'})

        if seller.id != review.product.seller_id:
            raise serializers.ValidationError('You can reply only to reviews for your own products.')

        attrs['seller'] = seller
        return attrs

    def save(self, review):
        seller = self.validated_data.get('seller')
        review.seller_reply_message = self.validated_data['message']
        review.seller_reply_name = (
            self.validated_data.get('seller_name')
            or getattr(getattr(seller, 'user', None), 'name', '')
            or getattr(getattr(seller, 'user', None), 'username', '')
            or 'Seller'
        )
        review.seller_reply_at = timezone.now()
        review.save(update_fields=['seller_reply_message', 'seller_reply_name', 'seller_reply_at', 'updated_at'])
        return review
