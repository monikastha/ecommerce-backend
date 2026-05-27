from django.db import models
from productcategory.models import Category

class Stock(models.Model):
    product_name = models.CharField(
        max_length=255, 
        default="Unknown Product"
    )
    
    quantity = models.IntegerField(default=0)
    
    # Made it nullable temporarily
    productcategory = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        related_name="stock",
        null=True,      # ← Added
        blank=True      # ← Added
    )
    
    availability_status = models.CharField(
        max_length=20,
        choices=[
            ('in_stock', 'In Stock'),
            ('low_stock', 'Low Stock'),
            ('out_of_stock', 'Out of Stock'),
        ],
        default='in_stock'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} - {self.quantity}"