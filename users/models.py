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

    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='buyer')
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class Staff(models.Model):

#     ROLE_CHOICES = (
#         ("assistant", "Assistant"),
#         ("warehousestaff", "Warehouse Staff"),
#     )

#     user = models.OneToOneField(
#         Users,
#         on_delete=models.CASCADE,
#         related_name="staff_profile"
#     )

#     phone = models.CharField(max_length=15, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     role = models.CharField(max_length=50, choices=ROLE_CHOICES)

#     created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username