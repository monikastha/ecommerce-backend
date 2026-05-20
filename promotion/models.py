from django.db import models
from django.utils import timezone

class Promotion(models.Model):
    TYPE_CHOICES = [
        ('percentage', 'Percentage Off'),
        ('fixed', 'Fixed Amount'),
        ('free_shipping', 'Free Shipping'),
        ('buy_x_get_y', 'Buy X Get Y'),
    ]

    APPLIES_CHOICES = [
        ('all', 'All Products'),
        ('category', 'Specific Categories'),
        ('product', 'Specific Products'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
    ]

    name = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)

    applies_to = models.CharField(max_length=20, choices=APPLIES_CHOICES, default='all')

    # Categories (Many-to-Many)
    categories = models.ManyToManyField(
        'product.Category',   # ← Change 'product' if your category app name is different
        blank=True,
        related_name='promotions'
    )

    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"

    def __str__(self):
        return self.name

    @property
    def is_expired(self):
        return self.end_date < timezone.now().date()

    def save(self, *args, **kwargs):
        if self.is_expired and self.status != 'expired':
            self.status = 'expired'
        super().save(*args, **kwargs)