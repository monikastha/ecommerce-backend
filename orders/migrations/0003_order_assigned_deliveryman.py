from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deliveryman', '0007_delete_deliverycharge'),
        ('orders', '0002_alter_order_payment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='assigned_deliveryman',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='assigned_orders',
                to='deliveryman.deliveryman',
            ),
        ),
    ]
