from decimal import Decimal, InvalidOperation

from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import DeliveryChargeRule, Location
from .serializers import DeliveryChargeRuleSerializer, LocationSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(province__icontains=search) |
                Q(city__icontains=search)
            )
        return queryset


class DeliveryChargeRuleViewSet(viewsets.ModelViewSet):
    queryset = DeliveryChargeRule.objects.select_related('location').all()
    serializer_class = DeliveryChargeRuleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        location = self.request.query_params.get('location')
        delivery_type = self.request.query_params.get('delivery_type')
        search = self.request.query_params.get('search', '')

        if location:
            queryset = queryset.filter(location_id=location)

        if delivery_type:
            queryset = queryset.filter(delivery_type=delivery_type)

        if search:
            queryset = queryset.filter(
                Q(location__name__icontains=search) |
                Q(location__province__icontains=search) |
                Q(location__city__icontains=search)
            )

        return queryset


@api_view(['POST'])
def calculate_delivery_charge(request):
    location_id = request.data.get('location')
    delivery_type = request.data.get('delivery_type', 'normal')
    product_total = request.data.get('product_total', 0)

    if not location_id:
        return Response({'error': 'Location is required'}, status=status.HTTP_400_BAD_REQUEST)

    if delivery_type not in ['normal', 'emergency']:
        return Response({'error': 'Invalid delivery type'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        total = Decimal(str(product_total))
    except (InvalidOperation, TypeError):
        return Response({'error': 'Invalid product total'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        location = Location.objects.get(id=location_id, status='Active')
    except Location.DoesNotExist:
        return Response({'error': 'Active location not found'}, status=status.HTTP_404_NOT_FOUND)

    rule = (
        DeliveryChargeRule.objects
        .filter(
            location=location,
            delivery_type=delivery_type,
            status='Active',
            min_product_total__lte=total,
        )
        .filter(Q(max_product_total__isnull=True) | Q(max_product_total__gte=total))
        .order_by('-min_product_total')
        .first()
    )

    if not rule:
        return Response(
            {'error': 'No delivery charge rule found for this location and order total'},
            status=status.HTTP_404_NOT_FOUND
        )

    return Response({
        'location': location.id,
        'location_name': location.name,
        'province': location.province,
        'city': location.city,
        'delivery_type': delivery_type,
        'product_total': str(total),
        'delivery_charge': str(rule.charge),
        'rule_id': rule.id,
        'final_total': str(total + rule.charge),
    })
