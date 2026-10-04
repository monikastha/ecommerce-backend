from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('orders', '0008_order_delivery_proof'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_proof_photo',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_proof_uploaded_at',
        ),
    ]
