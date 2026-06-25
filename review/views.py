from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Case, IntegerField, Value, When
from .models import Review
from .serializers import ReviewReplySerializer, ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('product').all()
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        product = self.request.query_params.get('product')
        seller = self.request.query_params.get('seller')
        sentiment = self.request.query_params.get('sentiment')
        if product:
            queryset = queryset.filter(product_id=product)
        if seller:
            queryset = queryset.filter(product__seller_id=seller)
        if sentiment:
            queryset = queryset.filter(sentiment=sentiment)
        return queryset.annotate(
            sentiment_rank=Case(
                When(sentiment='positive', then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        ).order_by('sentiment_rank', '-rating', '-created_at')

    @action(detail=True, methods=['post'], url_path='reply')
    def reply(self, request, pk=None):
        review = self.get_object()
        serializer = ReviewReplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(review)
        return Response(ReviewSerializer(review, context={'request': request}).data)
