from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='CommissionSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'commission_rate',
                    models.DecimalField(
                        decimal_places=2,
                        default=10.0,
                        help_text='Commission percentage (e.g., 10 means 10%)',
                        max_digits=5,
                    ),
                ),
                (
                    'normal_delivery_charge',
                    models.DecimalField(
                        decimal_places=2,
                        default=200.0,
                        help_text='Standard delivery charge in Rs.',
                        max_digits=10,
                    ),
                ),
                (
                    'emergency_delivery_charge',
                    models.DecimalField(
                        decimal_places=2,
                        default=500.0,
                        help_text='Emergency/Fast delivery charge in Rs.',
                        max_digits=10,
                    ),
                ),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Commission Settings',
            },
        ),
    ]
