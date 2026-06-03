from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_stock_product_location_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='available_to_buyers',
            field=models.BooleanField(default=True),
        ),
    ]
