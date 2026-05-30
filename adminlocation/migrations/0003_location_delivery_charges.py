from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminlocation', '0002_alter_location_options_alter_location_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='emergency_delivery_charge',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='location',
            name='normal_delivery_charge',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
