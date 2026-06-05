from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'buyer_username', 'total', 'status', 'payment_type', 'created_at')
    list_filter = ('status', 'payment_type', 'delivery_type', 'created_at')
    search_fields = ('order_number', 'customer_name', 'email', 'phone', 'buyer_username', 'user__username')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'quantity', 'price', 'subtotal')
    search_fields = ('order__order_number', 'product_name')
