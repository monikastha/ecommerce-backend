from decimal import Decimal

from django.db import migrations, models


def backfill_commission_rate(apps, schema_editor):
    Order = apps.get_model('orders', 'Order')
    CommissionSettings = apps.get_model('earnings', 'CommissionSettings')
    settings = CommissionSettings.objects.filter(id=1).first()
    commission_rate = settings.commission_rate if settings else Decimal('10.00')
    Order.objects.filter(commission_rate=0).update(commission_rate=commission_rate)


class Migration(migrations.Migration):

    dependencies = [
        ('earnings', '0001_initial'),
        ('orders', '0005_alter_order_status_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='commission_rate',
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                help_text='Commission percentage applied when this order was placed.',
                max_digits=5,
            ),
        ),
        migrations.RunPython(backfill_commission_rate, migrations.RunPython.noop),
    ]
