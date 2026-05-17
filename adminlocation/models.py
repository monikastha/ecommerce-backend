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