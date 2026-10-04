from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.views.decorators.http import require_http_methods
import datetime


@require_http_methods(["POST", "GET"])
def send_test_notification(request):
    channel_layer = get_channel_layer()
    payload = {
        'type': 'notification_message',
        'message': {
            'event': 'test_notification',
            'order_id': 0,
            'order_number': f'TEST-{datetime.datetime.utcnow().isoformat()}',
            'total': '0',
            'delivery_type': 'normal',
            'created_at': datetime.datetime.utcnow().isoformat(),
        }
    }
    try:
        async_to_sync(channel_layer.group_send)('assistant_notifications', payload)
        return JsonResponse({'ok': True})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)
