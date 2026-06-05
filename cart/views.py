from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from adminlocation.models import Location
from product.models import Product
from stock.models import Stock
from .models import Cart, CartItem
from .serializers import CartSerializer

User = get_user_model()


class CartViewSet(viewsets.ViewSet):
    def _positive_int(self, value, default=1):
        try:
            parsed = int(value or default)
        except (TypeError, ValueError):
            return None
        return parsed if parsed > 0 else None

    def _identifier(self, request):
        user_id = request.query_params.get('user_id') or request.data.get('user_id')
        username = request.query_params.get('username') or request.data.get('username')
        if request.user and request.user.is_authenticated:
            return request.user, request.user.username
        if user_id:
            try:
                user = User.objects.get(id=user_id, role='buyer')
                return user, user.username
            except User.DoesNotExist:
                return None, None
        if username:
            try:
                user = User.objects.get(username=username, role='buyer')
                return user, user.username
            except User.DoesNotExist:
                return None, username
        return None, None

    def _cart(self, request):
        user, username = self._identifier(request)
        if user:
            cart, _ = Cart.objects.get_or_create(user=user, defaults={'buyer_username': user.username})
            if cart.buyer_username != user.username:
                cart.buyer_username = user.username
                cart.save(update_fields=['buyer_username', 'updated_at'])
            return cart
        if username:
            cart, _ = Cart.objects.get_or_create(user=None, buyer_username=username)
            return cart
        return None

    def _serialized_cart(self, cart, request, http_status=status.HTTP_200_OK):
        cart = Cart.objects.prefetch_related('items__product__category').get(pk=cart.pk)
        return Response(CartSerializer(cart, context={'request': request}).data, status=http_status)

    def list(self, request):
        cart = self._cart(request)
        if not cart:
            return Response({'error': 'Provide buyer user_id or username'}, status=status.HTTP_400_BAD_REQUEST)
        return self._serialized_cart(cart, request)

    def create(self, request):
        return self.add_item(request)

    @action(detail=False, methods=['post'], url_path='add-item')
    def add_item(self, request):
        cart = self._cart(request)
        if not cart:
            return Response({'error': 'Provide buyer user_id or username'}, status=status.HTTP_400_BAD_REQUEST)

        product_id = request.data.get('product')
        quantity = self._positive_int(request.data.get('quantity'), 1)
        location_id = request.data.get('location')
        location_name = request.data.get('location_name', '')

        if not quantity:
            return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id, status='approved', is_published=True)
        except Product.DoesNotExist:
            return Response({'error': 'Product is not available'}, status=status.HTTP_404_NOT_FOUND)

        stock = Stock.objects.filter(product=product, available_to_buyers=True).first()
        if not stock or stock.quantity < quantity:
            return Response({'error': 'Out of Stock'}, status=status.HTTP_400_BAD_REQUEST)

        location = None
        if location_id:
            location = Location.objects.filter(id=location_id).first()
            if not location:
                return Response({'error': 'Delivery location not found'}, status=status.HTTP_404_NOT_FOUND)
            location_name = location_name or f'{location.name}, {location.city}'

        with transaction.atomic():
            item, created = CartItem.objects.select_for_update().get_or_create(
                cart=cart,
                product=product,
                defaults={
                    'quantity': quantity,
                    'price_snapshot': product.price,
                    'location': location,
                    'location_name': location_name,
                },
            )
            if not created:
                next_quantity = item.quantity + quantity
                if stock.quantity < next_quantity:
                    return Response({'error': 'Quantity exceeds available stock'}, status=status.HTTP_400_BAD_REQUEST)
                item.quantity = next_quantity
                item.price_snapshot = product.price
                item.location = location or item.location
                item.location_name = location_name or item.location_name
                item.save(update_fields=['quantity', 'price_snapshot', 'location', 'location_name', 'updated_at'])

        return self._serialized_cart(cart, request, status.HTTP_201_CREATED)

    @action(detail=False, methods=['patch', 'post'], url_path='update-item')
    def update_item(self, request):
        cart = self._cart(request)
        if not cart:
            return Response({'error': 'Provide buyer user_id or username'}, status=status.HTTP_400_BAD_REQUEST)

        item_id = request.data.get('item_id') or request.query_params.get('item_id')
        product_id = request.data.get('product') or request.query_params.get('product')
        quantity = self._positive_int(request.data.get('quantity') or request.query_params.get('quantity'), None)

        if not quantity:
            return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)

        item = CartItem.objects.filter(cart=cart, id=item_id).first() if item_id else CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if not item:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

        stock = Stock.objects.filter(product=item.product, available_to_buyers=True).first()
        if not stock or stock.quantity < quantity:
            return Response({'error': 'Quantity exceeds available stock'}, status=status.HTTP_400_BAD_REQUEST)

        item.quantity = quantity
        item.save(update_fields=['quantity', 'updated_at'])
        return self._serialized_cart(cart, request)

    @action(detail=False, methods=['post', 'delete'], url_path='remove-item')
    def remove_item(self, request):
        cart = self._cart(request)
        if not cart:
            return Response({'error': 'Provide buyer user_id or username'}, status=status.HTTP_400_BAD_REQUEST)

        item_id = request.data.get('item_id') or request.query_params.get('item_id')
        product_id = request.data.get('product') or request.query_params.get('product')
        item = CartItem.objects.filter(cart=cart, id=item_id).first() if item_id else CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if not item:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return self._serialized_cart(cart, request)

    @action(detail=False, methods=['post', 'delete'], url_path='clear')
    def clear(self, request):
        cart = self._cart(request)
        if not cart:
            return Response({'error': 'Provide buyer user_id or username'}, status=status.HTTP_400_BAD_REQUEST)

        cart.items.all().delete()
        return self._serialized_cart(cart, request)
