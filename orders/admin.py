from django.contrib import admin, messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import ngettext

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
    actions = [
        'set_status_created',
        'set_status_in_progress',
        'set_status_ready_for_pickup',
        'set_status_completed'
    ]

    @admin.action(description="Set status to 'Created'")
    def set_status_created(self, request, queryset):
        updated = queryset.update(status='created')
        # send email status update
        for order in queryset:
            send_email_status_update(order)
        self.message_user(request, ngettext(
            '%d order was successfully marked as created.',
            '%d orders were successfully marked as created.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description="Set status to 'In Progress'")
    def set_status_in_progress(self, request, queryset):
        updated = queryset.update(status='in-progress')
        # send email status update
        for order in queryset:
            send_email_status_update(order)
        self.message_user(request, ngettext(
            '%d order was successfully marked as in-progress.',
            '%d orders were successfully marked as in-progress.',
            updated
        ) % updated, messages.SUCCESS)

    @admin.action(description="Set status to 'Ready for Pickup'")
    def set_status_ready_for_pickup(self, request, queryset):
        updated = queryset.update(status='ready-for-pickup')
        # send email status update
        for order in queryset:
            send_email_status_update(order)
        self.message_user(request, ngettext(
            '%d order was successfully marked as ready for pickup.',
            '%d orders were successfully marked as ready for pickup.',
            updated,
        ) % updated, messages.SUCCESS)

    @admin.action(description="Set status to 'Completed'")
    def set_status_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        # send email status update
        for order in queryset:
            send_email_status_update(order)
        self.message_user(request, ngettext(
            '%d order was successfully marked as completed.',
            '%d orders were successfully marked as completed.',
            updated
        ) % updated, messages.SUCCESS)


admin.site.register(Order, OrderAdmin)


def send_email_status_update(order):
    html_message = render_to_string('orders/emails/order_update.html', {'order': order})
    send_mail(
        f'Order: {order.code} Update | Macalicious',
        strip_tags(html_message),
        "Macalicious <shop.macalicious@gmail.com>",
        ['shop.macalicious@gmail.com', order.user.email],
        fail_silently=True,
        html_message=html_message
    )
