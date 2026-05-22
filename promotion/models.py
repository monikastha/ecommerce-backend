from django.db import models
from django.utils import timezone

class Promotion(models.Model):

    TYPE_CHOICES = [
        ('percentage', 'Percentage Off'),
        ('fixed', 'Fixed Amount Off'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expired', 'Expired'),
    ]

    APPLIES_CHOICES = [
        ('all', 'All Products'),
        ('category', 'Specific Categories'),
    ]

    name = models.CharField(max_length=200, unique=True)

    d_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    d_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    applies_to = models.CharField(max_length=20, choices=APPLIES_CHOICES, default='all')

    categories = models.ManyToManyField(
        'productcategory.Category',
        blank=True,
        related_name='promotions'
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_expired(self):
        return timezone.now() > self.end_date