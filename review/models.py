from django.db import models
from product.models import Product


POSITIVE_WORDS = {
    'good', 'great', 'excellent', 'amazing', 'nice', 'love', 'loved', 'best',
    'perfect', 'quality', 'satisfied', 'happy', 'recommend', 'fast', 'beautiful',
}
NEGATIVE_WORDS = {
    'bad', 'poor', 'worst', 'broken', 'damaged', 'late', 'slow', 'fake',
    'cheap', 'disappointed', 'disappointing', 'refund', 'return', 'problem',
}


def detect_sentiment(message, rating):
    words = {word.strip(".,!?;:'\"()[]{}").lower() for word in (message or '').split()}
    positive_hits = len(words & POSITIVE_WORDS)
    negative_hits = len(words & NEGATIVE_WORDS)

    if positive_hits > negative_hits:
        return 'positive'
    if negative_hits > positive_hits:
        return 'negative'
    return 'positive' if rating >= 3 else 'negative'

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
    seller_reply_message = models.TextField(blank=True)
    seller_reply_name = models.CharField(max_length=150, blank=True)
    seller_reply_at = models.DateTimeField(null=True, blank=True)
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
        self.sentiment = detect_sentiment(self.review_message, self.rating)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rating} - {self.review_message[:70]}"
