from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('adminlocation', '0005_remove_location_emergency_delivery_charge_and_more'),
        ('product', '0006_alter_product_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=40, unique=True)),
                ('buyer_username', models.CharField(blank=True, db_index=True, max_length=150)),
                ('customer_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=30)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=100)),
                ('postal_code', models.CharField(max_length=30)),
                ('delivery_location_name', models.CharField(blank=True, max_length=255)),
                ('delivery_type', models.CharField(choices=[('normal', 'Normal Delivery'), ('emergency', 'Emergency Fast Delivery')], default='normal', max_length=20)),
                ('delivery_fee', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('payment_type', models.CharField(choices=[('cash_on_delivery', 'Cash on Delivery')], default='cash_on_delivery', max_length=30)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('processing', 'Processing'), ('shipped', 'Shipped'), ('out_for_delivery', 'Out For Delivery'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='confirmed', max_length=30)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('delivery_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='adminlocation.location')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200)),
                ('product_category', models.CharField(blank=True, max_length=150)),
                ('product_image', models.URLField(blank=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('subtotal', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='product.product')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
