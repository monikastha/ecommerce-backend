from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('assistant', 'Assistant'),
        ('warehousestaff', 'WarehouseStaff'),
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('delivery', 'Deliveryman'),
    )

    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='buyer')

    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username