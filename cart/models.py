import decimal

from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .managers import CartManager, CartItemManager


class Cart(models.Model):
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    number_of_items = models.PositiveIntegerField(default=0)
    total = models.DecimalField(default=0.0, max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return f"Cart ID: {self.id}"

    def display_total(self):
        return mark_safe(f"${self.total}")

    def admin_total(self):
        return mark_safe(f"<span style='font-size:14px;color:#fb523b;font-weight:bold;'>${self.total}</span>")

    admin_total.short_description = "Total"

    def admin_cart_items(self):
        output = ""
        for item in self.cart_items.all():
            output += f"<li>{item.content_object.get_name()} &nbsp;({item.quantity})</li>"
        return mark_safe(output)

    admin_cart_items.short_description = "Cart Items"


###
# CartItem needs to be generic in order to add:
#     - MacaronSet
#     - MacaronCollection
###
class CartItem(models.Model):
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    item_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("item_type", "object_id")
    quantity = models.PositiveIntegerField(default=1)
    total = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)
    slug = models.SlugField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CartItemManager()

    def __str__(self):
        return f"Cart: {self.id}"

    def get_quantity(self):
        return f"Quantity: {self.quantity}"

    def get_total(self):
        return self.quantity * self.content_object.get_total()

    def display_total(self):
        if self.content_object.is_on_sale():
            return mark_safe(f"<span style='color:#b53211;'>${self.get_total()}</span>")
        else:
            return mark_safe(f"<span>${self.get_total()}</span>")

    def display_total_checkout(self):
        return self.quantity

    def admin_cart_item(self):
        return f"CartItem: {self.id}"

    admin_cart_item.short_description = "Item"

    def admin_total(self):
        if self.total > 0:
            return mark_safe(f"<span style='font-size:14px;color:#fb523b;font-weight:bold;'>${self.total}</span>")
        else:
            return 0

    admin_total.short_description = "Total"

    def admin_user(self):
        if self.cart.user:
            return f"{self.cart.user.username}"
        else:
            return '-'

    admin_user.short_description = "User"

    def admin_item_type(self):
        return f"{self.item_type.name}"

    admin_item_type.short_description = "Item Type"
