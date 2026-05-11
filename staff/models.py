from django.db import models

class Staff(models.Model):
    ROLE_CHOICES = (
        ('staff', 'Staff'),
        ('assistant', 'Assistant'),
    )

    username = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username