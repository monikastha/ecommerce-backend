from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productcategory', '0003_delete_subcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='requires_size',
            field=models.BooleanField(default=False),
        ),
    ]
