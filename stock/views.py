from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Stock
from .serializers import StockSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.select_related('product__category', 'location').all().order_by('-updated_at')
    serializer_class = StockSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        product = self.request.query_params.get('product')
        location = self.request.query_params.get('location')
        available = self.request.query_params.get('available')

        if product:
            queryset = queryset.filter(product_id=product)
        if location:
            queryset = queryset.filter(location_id=location)
        if available == 'true':
            queryset = queryset.filter(quantity__gt=0)

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
        location = data.get('location')
        quantity = int(data.get('quantity') or 0)
        data['availability_status'] = self._status_for_quantity(quantity)

        existing = Stock.objects.filter(product_id=product, location_id=location).first()
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
        data = request.data.copy()
        quantity = int(data.get('quantity') or 0)
        data['availability_status'] = self._status_for_quantity(quantity)
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def reduce(self, request, pk=None):
        stock = self.get_object()
        amount = int(request.data.get('quantity') or 1)
        if amount < 1:
            return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)

        stock.quantity = max(0, stock.quantity - amount)
        stock.availability_status = self._status_for_quantity(stock.quantity)
        stock.save(update_fields=['quantity', 'availability_status', 'updated_at'])
        return Response(self.get_serializer(stock).data)

    @action(detail=False, methods=['post'], url_path='reduce-by-location')
    def reduce_by_location(self, request):
        product = request.data.get('product')
        location = request.data.get('location')
        amount = int(request.data.get('quantity') or 1)

        if not product or not location:
            return Response({'error': 'Product and location are required'}, status=status.HTTP_400_BAD_REQUEST)
        if amount < 1:
            return Response({'error': 'Quantity must be at least 1'}, status=status.HTTP_400_BAD_REQUEST)

        stock = Stock.objects.filter(product_id=product, location_id=location).first()
        if not stock or stock.quantity < amount:
            return Response({'error': 'Out of Stock in Your Area'}, status=status.HTTP_400_BAD_REQUEST)

        stock.quantity -= amount
        stock.availability_status = self._status_for_quantity(stock.quantity)
        stock.save(update_fields=['quantity', 'availability_status', 'updated_at'])
        return Response(self.get_serializer(stock).data)
