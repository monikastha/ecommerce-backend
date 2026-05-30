from django.db import models
from product.models import Product

class Review(models.Model):
    SENTIMENT_CHOICES = (
        ('positive', 'Positive'),
        ('negative', 'Negative'),
    )
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True
    )
    buyer_username = models.CharField(max_length=150, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    review_message = models.TextField()
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, default='positive')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.sentiment = 'positive' if self.rating >= 3 else 'negative'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rating} - {self.review_message[:70]}"
