from .models import Cart


def cart_information(request):
    if request.session.get('cart'):
        try:
            cart = Cart.objects.get(id=request.session.get('cart'))
            return {
                'number_of_items': cart.number_of_items,
                'cart': cart,
            }
        except Cart.DoesNotExist:
            return {}
    return {}

