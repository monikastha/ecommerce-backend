from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Stock
from .serializers import StockSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.select_related('product__category').all().order_by('-updated_at')
    serializer_class = StockSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        product = self.request.query_params.get('product')
        available = self.request.query_params.get('available')

        if product:
            queryset = queryset.filter(product_id=product)
        if available == 'true':
            queryset = queryset.filter(quantity__gt=0, available_to_buyers=True)

        return queryset

    def _status_for_quantity(self, quantity):
        if quantity <= 0:
            return 'out_of_stock'
        if quantity < 10:
            return 'low_stock'
        return 'in_stock'

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        product = data.get('product')
        quantity = int(data.get('quantity') or 0)
        data['availability_status'] = self._status_for_quantity(quantity)

        existing = Stock.objects.filter(product_id=product).first()
        if existing:
            serializer = self.get_serializer(existing, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        if 'quantity' in data:
            quantity = int(data.get('quantity') or 0)
            data['availability_status'] = self._status_for_quantity(quantity)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def reduce(self, request, pk=None):
        amount = int(request.data.get('quantity') or 1)
        if amount < 1:
            return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            stock = Stock.objects.select_for_update().get(pk=pk)
            stock.quantity = max(0, stock.quantity - amount)
            stock.availability_status = self._status_for_quantity(stock.quantity)
            stock.save(update_fields=['quantity', 'availability_status', 'updated_at'])

        return Response(self.get_serializer(stock).data)

    @action(detail=False, methods=['post'], url_path='reduce-by-product')
    def reduce_by_product(self, request):
        product = request.data.get('product')
        amount = int(request.data.get('quantity') or 1)

        if not product:
            return Response({'error': 'Product is required'}, status=status.HTTP_400_BAD_REQUEST)
        if amount < 1:
            return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            stock = Stock.objects.select_for_update().filter(product_id=product).first()
            if not stock:
                return Response({'error': 'No inventory record found for this product'}, status=status.HTTP_400_BAD_REQUEST)
            if not stock.available_to_buyers:
                return Response({'error': 'This product is not available to buyers'}, status=status.HTTP_400_BAD_REQUEST)
            if stock.quantity < amount:
                return Response({'error': 'Out of Stock'}, status=status.HTTP_400_BAD_REQUEST)

            stock.quantity -= amount
            stock.availability_status = self._status_for_quantity(stock.quantity)
            stock.save(update_fields=['quantity', 'availability_status', 'updated_at'])

        return Response(self.get_serializer(stock).data)

    @action(detail=False, methods=['post'], url_path='reduce-by-location')
    def reduce_by_location(self, request):
        return self.reduce_by_product(request)
