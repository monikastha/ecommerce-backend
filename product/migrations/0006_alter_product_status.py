from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_product_seller_code_quantity_image_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(
                choices=[
                    ('pending', 'Pending'),
                    ('approved', 'Approved'),
                    ('rejected', 'Rejected'),
                    ('flagged', 'Flagged'),
                ],
                default='pending',
                max_length=20,
            ),
        ),
    ]
