from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'method', 'total', 'status', 'order_id', 'transaction_id', 'date')
    list_filter = ('method', 'status', 'date')
    search_fields = ('order_id', 'transaction_id')
    readonly_fields = ('date', 'created_at', 'updated_at')
    ordering = ('-created_at',)
