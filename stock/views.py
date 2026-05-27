from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Stock
from .serializers import StockSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def create(self, request, *args, **kwargs):
        # Optional: Auto update availability status
        quantity = request.data.get('quantity', 0)
        if quantity == 0:
            request.data['availability_status'] = 'out_of_stock'
        elif quantity < 10:
            request.data['availability_status'] = 'low_stock'
        
        return super().create(request, *args, **kwargs)