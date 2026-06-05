from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'buyer_username', 'item_count', 'total', 'updated_at')
    search_fields = ('buyer_username', 'user__username', 'user__email')
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity', 'price_snapshot', 'subtotal', 'updated_at')
    search_fields = ('product__name', 'cart__buyer_username', 'cart__user__username')
