from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(
                choices=[
                    ('cash_on_delivery', 'Cash on Delivery'),
                    ('khalti', 'Khalti'),
                ],
                default='cash_on_delivery',
                max_length=30,
            ),
        ),
    ]
