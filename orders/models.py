from django.conf import settings
from django.db import models
from adminlocation.models import Location
from product.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out For Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_CHOICES = (
        ('cash_on_delivery', 'Cash on Delivery'),
    )

    DELIVERY_CHOICES = (
        ('normal', 'Normal Delivery'),
        ('emergency', 'Emergency Fast Delivery'),
    )

    order_number = models.CharField(max_length=40, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True,
        blank=True,
    )
    buyer_username = models.CharField(max_length=150, blank=True, db_index=True)

    customer_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=30)

    delivery_location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_location_name = models.CharField(max_length=255, blank=True)
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='normal')
    delivery_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    payment_type = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='cash_on_delivery')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='confirmed')
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='order_items', null=True, blank=True)
    product_name = models.CharField(max_length=200)
    product_category = models.CharField(max_length=150, blank=True)
    product_image = models.URLField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'
