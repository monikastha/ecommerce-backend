from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminlocation', '0002_alter_location_options_alter_location_city_and_more'),
        ('product', '0005_product_seller_code_quantity_image_status_and_more'),
        ('stock', '0002_stock_product_name_stock_productcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='product_name',
            field=models.CharField(blank=True, default='Unknown Product', max_length=255),
        ),
        migrations.AddField(
            model_name='stock',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_stocks', to='adminlocation.location'),
        ),
        migrations.AddField(
            model_name='stock',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='location_stocks', to='product.product'),
        ),
        migrations.AddConstraint(
            model_name='stock',
            constraint=models.UniqueConstraint(fields=('product', 'location'), name='unique_product_location_stock'),
        ),
    ]
