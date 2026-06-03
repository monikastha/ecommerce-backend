from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Product
from .serializers import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category', 'seller__user').all().order_by('-id')
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'code', 'description', 'category__name', 'seller__user__name']
    filterset_fields = ['seller', 'category', 'status', 'is_published']

    def perform_create(self, serializer):
        serializer.save(status='pending', is_published=False, rejection_reason='')

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        product = self.get_object()
        product.status = 'approved'
        product.is_published = True
        product.rejection_reason = ''
        product.save(update_fields=['status', 'is_published', 'rejection_reason', 'updated_at'])
        return Response({
            'message': 'Product approved successfully',
            'product': self.get_serializer(product).data,
        })

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        product = self.get_object()
        product.status = 'rejected'
        product.is_published = False
        product.rejection_reason = request.data.get('rejection_reason', '')
        product.save(update_fields=['status', 'is_published', 'rejection_reason', 'updated_at'])
        return Response({
            'message': 'Product rejected successfully',
            'product': self.get_serializer(product).data,
        })

    @action(detail=True, methods=['post'])
    def flag(self, request, pk=None):
        product = self.get_object()
        product.status = 'flagged'
        product.is_published = False
        product.rejection_reason = request.data.get(
            'reason',
            'Flagged as inappropriate by admin/assistant',
        )
        product.save(update_fields=['status', 'is_published', 'rejection_reason', 'updated_at'])
        return Response({
            'message': 'Product flagged as inappropriate',
            'product': self.get_serializer(product).data,
        })

    @action(detail=True, methods=['delete', 'post'], url_path='remove')
    def remove(self, request, pk=None):
        product = self.get_object()
        product.delete()
        return Response({'message': 'Product removed successfully'})

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        product = self.get_object()
        if product.status != 'approved':
            return Response(
                {'error': 'Only approved products can be published'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        product.is_published = True
        product.save(update_fields=['is_published', 'updated_at'])
        return Response({'message': 'Product published successfully'})

    @action(detail=True, methods=['post'])
    def unpublish(self, request, pk=None):
        product = self.get_object()
        product.is_published = False
        product.save(update_fields=['is_published', 'updated_at'])
        return Response({'message': 'Product unpublished successfully'})
