# product/models.py
from django.db import models
from productcategory.models import Category
from seller.models import Seller

class Product(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('flagged', 'Flagged'),
    )

    seller = models.ForeignKey(
        Seller,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )
    name = models.CharField(max_length=10000)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name="products"
    )
    code = models.CharField(max_length=60, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(default=0)
    size = models.CharField(max_length=60, blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_published = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """Model to store multiple images/views for a product"""
    IMAGE_TYPE_CHOICES = (
        ('front', 'Front View'),
        ('back', 'Back View'),
        ('side', 'Side View'),
        ('top', 'Top View'),
        ('detail', 'Detail View'),
        ('other', 'Other View'),
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_images"
    )
    image = models.ImageField(upload_to='products/views/')
    image_type = models.CharField(
        max_length=20,
        choices=IMAGE_TYPE_CHOICES,
        default='other',
        help_text="Type of view/angle"
    )
    view_number = models.PositiveIntegerField(
        default=1,
        help_text="View order (1, 2, 3, etc.)"
    )
    is_primary = models.BooleanField(
        default=False,
        help_text="Set as primary/default image"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['view_number']
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"{self.product.name} - View {self.view_number}"


class ProductColor(models.Model):
    """Model to store color variants of a product"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="colors"
    )
    color_name = models.CharField(
        max_length=100,
        help_text="Name of the color (e.g., Red, Blue, Black)"
    )
    color_code = models.CharField(
        max_length=7,
        default='#000000',
        help_text="Hex color code (e.g., #FF0000)"
    )
    quantity = models.PositiveIntegerField(
        default=0,
        help_text="Available quantity in this color"
    )
    price_adjustment = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Price difference for this color (can be positive or negative)"
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Whether this color is available for sale"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['color_name']
        verbose_name = "Product Color"
        verbose_name_plural = "Product Colors"
        unique_together = ['product', 'color_name']

    def __str__(self):
        return f"{self.product.name} - {self.color_name}"
