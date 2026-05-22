# deliveryman/models.py
from django.db import models
from users.models import Users


class Deliveryman(models.Model):
    user = models.OneToOneField(
        Users,
        on_delete=models.CASCADE,
        related_name="delivery_profile",
        null=True,
        blank=True
    )
    
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Deliverymen"