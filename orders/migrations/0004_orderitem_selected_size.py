from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_assigned_deliveryman'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='selected_size',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]
