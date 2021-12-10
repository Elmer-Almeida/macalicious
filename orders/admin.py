from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'admin_cart', 'user', 'admin_num_cart_items', 'admin_num_cart_items_active', 'admin_tax_rate',
        'admin_total', 'status', 'active', 'created_at', 'updated_at'
    ]
    list_editable = [
        'active', 'status'
    ]
    list_filter = [
        'active', 'status'
    ]
    search_fields = [
        'user__username', 'user__email', 'user__first_name', 'user__last_name', 'code', 'status'
    ]
    readonly_fields = [
        'cart', 'user', 'total', 'tax', 'code', 'admin_num_cart_items', 'admin_cart_items', 'created_at', 'updated_at'
    ]


admin.site.register(Order, OrderAdmin)
