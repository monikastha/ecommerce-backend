from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_orderitem_selected_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending'),
                    ('confirmed', 'Confirmed'),
                    ('processing', 'Processing'),
                    ('shipped', 'Shipped'),
                    ('out_for_delivery', 'Out For Delivery'),
                    ('delivered', 'Delivered'),
                    ('cancelled', 'Cancelled'),
                ],
                default='pending',
                max_length=30,
            ),
        ),
    ]
