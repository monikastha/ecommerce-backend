from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_review_product_buyer_sentiment'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='seller_reply_message',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='review',
            name='seller_reply_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='review',
            name='seller_reply_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
