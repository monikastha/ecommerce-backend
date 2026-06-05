from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from cart.models import Cart
from .models import Order
from .serializers import OrderCreateSerializer, OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items').select_related('user', 'delivery_location').all()

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        return OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        username = self.request.query_params.get('username')
        status_value = self.request.query_params.get('status')

        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if username:
            queryset = queryset.filter(buyer_username=username)
        if status_value:
            queryset = queryset.filter(status=status_value)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(
            OrderSerializer(order, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=['post'], url_path='set-status')
    def set_status(self, request, pk=None):
        order = self.get_object()
        next_status = request.data.get('status')
        allowed = [value for value, _ in Order.STATUS_CHOICES]
        if next_status not in allowed:
            return Response({'error': 'Invalid order status'}, status=status.HTTP_400_BAD_REQUEST)

        order.status = next_status
        order.save(update_fields=['status', 'updated_at'])
        return Response(OrderSerializer(order, context={'request': request}).data)

    @action(detail=False, methods=['post'], url_path='from-cart')
    def from_cart(self, request):
        username = request.data.get('username')
        user_id = request.data.get('user_id')
        cart = None

        if user_id:
            cart = Cart.objects.prefetch_related('items__product').filter(user_id=user_id).first()
        if not cart and username:
            cart = Cart.objects.prefetch_related('items__product').filter(buyer_username=username).first()

        if not cart or not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data['items'] = []
        for item in cart.items.all():
            image = ''
            if item.product and item.product.image:
                image = request.build_absolute_uri(item.product.image.url)
            data['items'].append({
                'product': item.product_id,
                'quantity': item.quantity,
                'price': str(item.price_snapshot),
                'image': image,
            })
        data['clear_cart'] = True

        serializer = OrderCreateSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(
            OrderSerializer(order, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )
