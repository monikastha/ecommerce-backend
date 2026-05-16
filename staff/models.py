from django.db import models
from users.models import Users


class Staff(models.Model):
    ROLE_CHOICES = (
        ('warehousestaff', 'WarehouseStaff'),
        ('assistant', 'Assistant'),
    )
    user = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        related_name="staff_profile",
        null=True,               # ← Add this temporarily
        blank=True
    )
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    REQUIRED_FIELDS = ['name', 'username', 'email']

    def __str__(self):
        return self.username
