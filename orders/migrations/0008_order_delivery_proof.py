from django.db import migrations, models


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('orders', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_proof_photo',
            field=models.ImageField(blank=True, null=True, upload_to='orders/delivery_proofs/'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_proof_uploaded_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
