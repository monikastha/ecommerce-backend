import base64
import hashlib
import hmac
import json
from uuid import uuid4
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from decimal import Decimal, InvalidOperation

from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Payment


def _money(value):
    try:
        return Decimal(str(value)).quantize(Decimal('0.01'))
    except (InvalidOperation, TypeError, ValueError):
        return None


def _signature(message):
    digest = hmac.new(
        settings.ESEWA_SECRET_KEY.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256,
    ).digest()
    return base64.b64encode(digest).decode('utf-8')


@api_view(['POST'])
@permission_classes([AllowAny])
def record_cod_payment(request):
    order_id = str(request.data.get('orderId') or '').strip()
    amount = _money(request.data.get('amount'))

    if not order_id:
        return Response({'message': 'Order ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    if amount is None or amount < 0:
        return Response({'message': 'A valid payment amount is required.'}, status=status.HTTP_400_BAD_REQUEST)

    payment, _ = Payment.objects.update_or_create(
        transaction_id=f'COD-{order_id}',
        defaults={
            'method': 'cod',
            'total': amount,
            'status': 'pending',
            'order_id': order_id,
            'extra_data': {
                'customer_name': request.data.get('customerName', ''),
                'email': request.data.get('email', ''),
                'phone': request.data.get('phone', ''),
                'address': request.data.get('address', ''),
                'delivery_type': request.data.get('deliveryType', ''),
                'delivery_location': request.data.get('deliveryLocation', ''),
                'delivery_fee': request.data.get('deliveryFee', 0),
                'items': request.data.get('items', []),
                'note': 'Cash to be collected on delivery.',
            },
        },
    )

    return Response({
        'id': payment.id,
        'orderId': payment.order_id,
        'method': payment.method,
        'status': payment.status,
        'total': str(payment.total),
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def initiate_esewa(request):
    order_id = str(request.data.get('orderId') or '').strip()
    amount = _money(request.data.get('amount'))
    product_name = str(request.data.get('productName') or 'Ecommerce Order').strip()

    if not order_id:
        return Response({'message': 'Order ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    if amount is None or amount <= 0:
        return Response({'message': 'A valid payment amount is required.'}, status=status.HTTP_400_BAD_REQUEST)

    product_code = settings.ESEWA_PRODUCT_CODE
    transaction_uuid = f'{order_id}-{uuid4().hex}'
    signed_field_names = 'total_amount,transaction_uuid,product_code'
    total_amount = f'{amount:.2f}'
    message = (
        f'total_amount={total_amount},'
        f'transaction_uuid={transaction_uuid},'
        f'product_code={product_code}'
    )
    callback_query = urlencode({
        'orderId': order_id,
        'transaction_uuid': transaction_uuid,
    })

    Payment.objects.update_or_create(
        transaction_id=transaction_uuid,
        defaults={
            'method': 'esewa',
            'total': amount,
            'status': 'pending',
            'order_id': order_id,
            'extra_data': {
                'product_name': product_name,
                'customer_name': request.data.get('customerName', ''),
                'email': request.data.get('email', ''),
            },
        },
    )

    return Response({
        'paymentUrl': settings.ESEWA_PAYMENT_URL,
        'formData': {
            'amount': total_amount,
            'tax_amount': '0',
            'total_amount': total_amount,
            'transaction_uuid': transaction_uuid,
            'product_code': product_code,
            'product_service_charge': '0',
            'product_delivery_charge': '0',
            'success_url': f'{settings.FRONTEND_PAYMENT_SUCCESS_URL}?{callback_query}',
            'failure_url': f'{settings.FRONTEND_PAYMENT_FAILURE_URL}?{callback_query}',
            'signed_field_names': signed_field_names,
            'signature': _signature(message),
        },
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def initiate_khalti(request):
    order_id = str(request.data.get('orderId') or '').strip()
    amount = _money(request.data.get('amount'))
    product_name = str(request.data.get('productName') or 'Ecommerce Order').strip()

    if not order_id:
        return Response({'message': 'Order ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

    if amount is None or amount <= 0:
        return Response({'message': 'A valid payment amount is required.'}, status=status.HTTP_400_BAD_REQUEST)

    if not settings.KHALTI_SECRET_KEY:
        return Response(
            {'message': 'Khalti secret key is not configured in backend .env.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    purchase_order_id = f'{order_id}-{uuid4().hex}'
    amount_paisa = int(amount * 100)
    callback_query = urlencode({
        'orderId': order_id,
        'purchase_order_id': purchase_order_id,
    })

    payload = {
        'return_url': f'{settings.FRONTEND_PAYMENT_SUCCESS_URL}?{callback_query}',
        'website_url': settings.KHALTI_WEBSITE_URL,
        'amount': amount_paisa,
        'purchase_order_id': purchase_order_id,
        'purchase_order_name': product_name,
        'customer_info': {
            'name': request.data.get('customerName', '') or 'Customer',
            'email': request.data.get('email', '') or 'customer@example.com',
            'phone': request.data.get('phone', '') or '9800000000',
        },
    }

    api_request = Request(
        settings.KHALTI_INITIATE_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Key {settings.KHALTI_SECRET_KEY}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )

    try:
        with urlopen(api_request, timeout=20) as api_response:
            data = json.loads(api_response.read().decode('utf-8'))
    except HTTPError as error:
        error_body = error.read().decode('utf-8')
        try:
            error_data = json.loads(error_body)
        except json.JSONDecodeError:
            error_data = {'message': error_body or 'Khalti payment initiation failed.'}
        return Response(error_data, status=error.code)
    except URLError as error:
        return Response(
            {'message': f'Unable to connect to Khalti: {error.reason}'},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    Payment.objects.update_or_create(
        transaction_id=purchase_order_id,
        defaults={
            'method': 'khalti',
            'total': amount,
            'status': 'pending',
            'order_id': order_id,
            'extra_data': {
                'pidx': data.get('pidx', ''),
                'product_name': product_name,
                'customer_name': request.data.get('customerName', ''),
                'email': request.data.get('email', ''),
                'phone': request.data.get('phone', ''),
            },
        },
    )

    return Response({
        'paymentUrl': data.get('payment_url'),
        'pidx': data.get('pidx'),
        'purchaseOrderId': purchase_order_id,
    })
