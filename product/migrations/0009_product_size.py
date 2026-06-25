from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_merge_20260609_0730'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]
