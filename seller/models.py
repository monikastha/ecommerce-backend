from django.db import models
from users.models import Users

class Seller(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    citizenship = models.CharField(max_length=50)
    pan_no = models.CharField(max_length=50)
    address = models.TextField()
    logo = models.ImageField(upload_to='seller/logo/')
    business_certificate = models.FileField(upload_to='seller/docs/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email
