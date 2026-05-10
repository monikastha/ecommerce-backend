from rest_framework import viewsets
from .models import ProductCategory
from .serializers import ProductCategorySerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer