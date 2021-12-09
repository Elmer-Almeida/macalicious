from django.db.models.signals import post_save, pre_save

from macalicious.utils import unique_slug_generator

from .models import Cart, CartItem


def cart_item_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        prefix = "item_"
        instance.slug = unique_slug_generator(instance, prefix, instance.content_object.get_name())


pre_save.connect(cart_item_pre_save_receiver, sender=CartItem)


def cart_item_post_save_receiver(sender, instance, *args, **kwargs):
    cart = instance.cart
    total_items = 0  # Keep track of all items in the cart
    total_amount = 0  # Keep track of cart item line total for cart total
    # update cart items and total after each item gets added to the cart
    for item in cart.cart_items.all():
        total_items += 1
        total_amount += item.get_total()
    # update the cart with number of items and cart total
    cart.number_of_items = total_items
    cart.total = total_amount
    cart.save()


post_save.connect(cart_item_post_save_receiver, sender=CartItem)
