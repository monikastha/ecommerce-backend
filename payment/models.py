from django.db import models

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cod', 'Cash on Delivery'),
        ('esewa', 'Esewa'),
        ('khalti', 'Khalti'),
    )

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # For digital payments: store transaction details
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    order_id = models.CharField(max_length=100, blank=True, null=True)
    
    # Store extra payment data (JSON)
    extra_data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.method} - {self.total} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']
