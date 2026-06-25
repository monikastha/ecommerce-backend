from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_remove_khalti'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='method',
            field=models.CharField(
                choices=[
                    ('cod', 'Cash on Delivery'),
                    ('esewa', 'Esewa'),
                    ('khalti', 'Khalti'),
                ],
                max_length=20,
            ),
        ),
    ]
