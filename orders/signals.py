from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Order
from django.core.serializers.json import DjangoJSONEncoder
import json


def build_order_notification(instance: Order, action: str):
    order_type = 'Emergency' if instance.delivery_type == 'emergency' else 'Normal'
    if action == 'created':
        event_text = f'{order_type} order placed'
    else:
        event_text = f'{order_type} order completed'

    return {
        'type': 'notification_message',
        'message': {
            'event': event_text,
            'order_id': instance.id,
            'order_number': instance.order_number,
            'total': str(instance.total),
            'delivery_type': instance.delivery_type,
            'order_type': order_type,
            'created_at': instance.created_at.isoformat(),
        }
    }


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance: Order, **kwargs):
    if not instance.pk:
        instance._previous_status = None
        return
    previous = Order.objects.filter(pk=instance.pk).values_list('status', flat=True).first()
    instance._previous_status = previous


@receiver(post_save, sender=Order)
def order_post_save(sender, instance: Order, created, **kwargs):
    channel_layer = get_channel_layer()
    payload = None

    if created:
        payload = build_order_notification(instance, 'created')
    else:
        previous_status = getattr(instance, '_previous_status', None)
        if instance.status == 'delivered' and previous_status != 'delivered':
            payload = build_order_notification(instance, 'completed')

    if payload is None:
        return

    try:
        async_to_sync(channel_layer.group_send)('assistant_notifications', payload)
    except Exception:
        # In case channels not configured yet, ignore
        pass
