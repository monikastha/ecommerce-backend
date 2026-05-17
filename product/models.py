# product/models.py
from django.db import models
from productcategory.models import Category   # ← Correct import

# Example Product model (you can modify as needed)
class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name="products"
    )
    # Add other fields as per your requirement
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name