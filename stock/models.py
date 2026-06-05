from django.db import models
from productcategory.models import Category
from product.models import Product

class Stock(models.Model):
    product_name = models.CharField(
        max_length=255, 
        blank=True,
        default="Unknown Product"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stocks",
        null=True,
        blank=True
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
    available_to_buyers = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["product"],
                name="unique_product_stock"
            )
        ]

    def __str__(self):
        product_label = self.product.name if self.product else self.product_name
        return f"{product_label} - {self.quantity}"
