import decimal

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe

from cart.models import Cart

from .managers import OrdersManager


ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('in-progress', 'In Progress'),
    ('ready-for-pickup', 'Ready for Pickup'),
    ('completed', 'Completed')
)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order')
    tax = models.DecimalField(decimal_places=2, max_digits=3, default=0.0)
    total = models.DecimalField(decimal_places=2, max_digits=5, blank=True, null=True)
    code = models.CharField(unique=True, max_length=50)
    active = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = OrdersManager()

    def __str__(self):
        return f"{self.user}'s order | ID: {self.id} | {self.code}"

    def admin_cart(self):
        return f"{self.cart.id}"

    def get_tax_rate(self):
        return self.tax * 100

    def calculate_total(self):
        return (decimal.Decimal(self.tax) * self.cart.total) + self.cart.total

    def get_tax_amount(self):
        return decimal.Decimal(self.tax) * self.cart.total

    admin_cart.short_description = "Cart ID"

    def admin_tax_rate(self):
        return mark_safe(f"{self.tax * 100}%")

    admin_tax_rate.short_description = "Tax Rate"

    def admin_total(self):
        return mark_safe(f"<span style='font-size:14px;font-weight:bold;color:#fb523b;'>${self.total}</span>")

    admin_total.short_description = "Total"

    def admin_num_cart_items(self):
        return self.cart.cart_items.count()

    admin_num_cart_items.short_description = "Items Count"

    def admin_num_cart_items_active(self):
        return self.cart.cart_items.active().count()

    admin_num_cart_items_active.short_description = "Active Items Count"

    def admin_cart_items(self):
        output = ""
        for item in self.cart.cart_items.all():
            output += f"<li>{item.content_object.get_name()} &nbsp;({item.quantity})</li>"
        return mark_safe(output)

    admin_cart_items.short_description = "Cart Items"
