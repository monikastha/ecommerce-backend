from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_seller_code_quantity_image_status_and_more'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='buyer_username',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='review',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='product.product'),
        ),
        migrations.AddField(
            model_name='review',
            name='sentiment',
            field=models.CharField(choices=[('positive', 'Positive'), ('negative', 'Negative')], default='positive', max_length=20),
        ),
    ]
