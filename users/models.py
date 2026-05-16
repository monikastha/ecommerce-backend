from django.contrib.auth.models import AbstractUser
from django.db import models

class Users(AbstractUser):

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('assistant', 'Assistant'),
        ('warehousestaff', 'Warehouse Staff'),
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('delivery', 'Delivery Man'),
    )

    name  = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='buyer')
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    REQUIRED_FIELDS=['name','role', 'email']



    def __str__(self):
        return self.username