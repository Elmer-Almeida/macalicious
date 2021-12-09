from django.contrib import admin

from .models import Cart, CartItem
from .filters import ItemTypeFilter, PriceRangeFilter


class CartAdmin(admin.ModelAdmin):
    list_display = [
        '__str__', 'user', 'number_of_items', 'admin_total', 'active', 'created_at', 'updated_at'
    ]
    list_filter = [
        'active', PriceRangeFilter
    ]
    list_editable = [
        'active'
    ]
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name', 'user__email'
    ]
    readonly_fields = [
        'user', 'total', 'number_of_items', 'admin_cart_items', 'created_at', 'updated_at'
    ]


admin.site.register(Cart, CartAdmin)


class CartItemAdmin(admin.ModelAdmin):
    list_display = [
        'admin_cart_item', 'quantity', 'admin_total', 'cart', 'admin_user',
        'admin_item_type', 'active', 'created_at', 'updated_at'
    ]
    list_editable = [
        'active'
    ]
    readonly_fields = [
        'cart', 'admin_cart_item', 'quantity', 'total', 'slug', 'item_type', 'object_id', 'created_at', 'updated_at'
    ]
    list_filter = [
        'active', ItemTypeFilter, PriceRangeFilter
    ]
    search_fields = [
        'cart__user__username', 'cart__user__first_name', 'cart__user__last_name', 'cart__user__email'
    ]


admin.site.register(CartItem, CartItemAdmin)
