from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_payment_options_payment_extra_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.CharField(
                choices=[('cod', 'Cash on Delivery'), ('esewa', 'Esewa')],
                max_length=20,
            ),
        ),
        migrations.RemoveField(
            model_name='payment',
            name='pidx',
        ),
    ]
