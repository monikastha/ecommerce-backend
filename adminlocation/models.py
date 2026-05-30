from django.db import models

class Location(models.Model):
    PROVINCE_CHOICES = [
        ('Koshi', 'Koshi Province'),
        ('Madhesh', 'Madhesh Province'),
        ('Bagmati', 'Bagmati Province'),
        ('Gandaki', 'Gandaki Province'),
        ('Lumbini', 'Lumbini Province'),
        ('Karnali', 'Karnali Province'),
        ('Sudurpashchim', 'Sudurpashchim Province'),
    ]

    name = models.CharField(max_length=200, verbose_name="Location Name")
    province = models.CharField(
        max_length=20,
        choices=PROVINCE_CHOICES,
        verbose_name="Province"
    )
    city = models.CharField(max_length=100, verbose_name="City")
    status = models.CharField(
        max_length=10,
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive')
        ],
        default='Active'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.city} ({self.province})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Location"
        verbose_name_plural = "Locations"


class DeliveryChargeRule(models.Model):
    DELIVERY_TYPE_CHOICES = [
        ('normal', 'Normal Delivery'),
        ('emergency', 'Emergency Fast Delivery'),
    ]

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name='delivery_charge_rules',
        verbose_name='Location Zone'
    )
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES)
    min_product_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    max_product_total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=10,
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive')
        ],
        default='Active'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        max_total = self.max_product_total if self.max_product_total is not None else 'above'
        return f"{self.location} - {self.delivery_type} - {self.min_product_total} to {max_total}"

    class Meta:
        ordering = ['location__province', 'location__city', 'min_product_total']
        verbose_name = "Delivery Charge Rule"
        verbose_name_plural = "Delivery Charge Rules"
