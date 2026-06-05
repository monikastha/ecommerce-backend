from django.db import migrations, models


def merge_location_stock(apps, schema_editor):
    Stock = apps.get_model('stock', 'Stock')

    product_ids = (
        Stock.objects
        .exclude(product_id__isnull=True)
        .values_list('product_id', flat=True)
        .distinct()
    )

    for product_id in product_ids:
        rows = list(Stock.objects.filter(product_id=product_id).order_by('id'))
        if len(rows) <= 1:
            continue

        keeper = rows[0]
        quantity = sum(row.quantity for row in rows)
        keeper.quantity = quantity
        keeper.available_to_buyers = any(row.available_to_buyers for row in rows)
        if quantity <= 0:
            keeper.availability_status = 'out_of_stock'
        elif quantity < 10:
            keeper.availability_status = 'low_stock'
        else:
            keeper.availability_status = 'in_stock'
        keeper.save(update_fields=['quantity', 'available_to_buyers', 'availability_status', 'updated_at'])

        Stock.objects.filter(id__in=[row.id for row in rows[1:]]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0004_stock_available_to_buyers'),
    ]

    operations = [
        migrations.RunPython(merge_location_stock, migrations.RunPython.noop),
        migrations.RemoveConstraint(
            model_name='stock',
            name='unique_product_location_stock',
        ),
        migrations.RemoveField(
            model_name='stock',
            name='location',
        ),
        migrations.AddConstraint(
            model_name='stock',
            constraint=models.UniqueConstraint(fields=('product',), name='unique_product_stock'),
        ),
    ]
