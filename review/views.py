from rest_framework import viewsets
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('product').all().order_by('-created_at')
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        product = self.request.query_params.get('product')
        sentiment = self.request.query_params.get('sentiment')
        if product:
            queryset = queryset.filter(product_id=product)
        if sentiment:
            queryset = queryset.filter(sentiment=sentiment)
        return queryset
