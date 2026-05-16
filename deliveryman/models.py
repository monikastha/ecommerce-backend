from django.db import models
class Deliveryman(models.Model):
    
    name = models.CharField(max_length=150)
    username = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=255) 
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username