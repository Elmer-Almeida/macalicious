import json
import urllib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import mark_safe, strip_tags
from django.views.generic import View

from macalicious.utils import random_string_generator
from orders.models import Order
from shop.models import MacaronSet
from .forms import AddToCartForm
from .models import Cart, CartItem


# add macaron set or collection to the cart
# if a cart instance is not saved in request.session, create a new cart instance
def add_to_card(request, slug):
    if request.method == "POST":
        # Check if the quantity of the item being added is valid
        if int(request.POST.get('quantity')) > 0:
            cart_instance = get_or_create_cart(request)
            try:
                # Get the contenttype instance type
                item_type = ContentType.objects.get(model=request.POST.get('item_type'))
            except ContentType.DoesNotExist:
                return HttpResponse("Something went wrong.")
            # get the model class from the contenttype instance type
            Klass = item_type.model_class()
            # get the object based on the slug provided
            object_instance = Klass.objects.get(slug=slug)
            object_id = object_instance.id

            # get the object name being added to the cart.
            object_name = get_object_name(item_type=request.POST.get('item_type'), object_instance=object_instance)

            add_to_cart_form = AddToCartForm(data=request.POST)
            if add_to_cart_form.is_valid():
                # create the CartItem instance
                cart_item = add_to_cart_form.save(commit=False)
                # add cart item details
                cart_item.cart = cart_instance
                cart_item.item_type = item_type
                cart_item.object_id = object_id
                cart_item.total = cart_item.get_total()
                cart_item.save()
                # check if user is logged in
                if request.user.is_authenticated:
                    # associate logged in user to cart
                    cart_item.cart.user = request.user
                    cart_item.save()
                messages.add_message(request, messages.SUCCESS, mark_safe(
                    f"<i class='bi bi-cart-check'></i>&nbsp; {object_name} has been added to the cart"))
                return redirect(reverse('cart:view'))
            else:
                # Adding to cart is invalid
                messages.add_message(request, messages.ERROR,
                                     f"There was an issue adding {object_instance.name} to your cart")
                return redirect(reverse('cart:view'))
        else:
            # Quantity is invalid.
            messages.add_message(request, messages.ERROR, f"Please choose a valid quantity. One or more required.")
            return redirect(reverse('shop:view'))
    else:
        # GET request is invalid
        messages.add_message(request, messages.ERROR, f"Something went wrong. Please try again later.")
        return redirect(reverse('cart:view'))


# Get cart stored in request.session or create a cart and store it in request.session
def get_or_create_cart(request):
    if request.session.get('cart'):
        try:
            cart = Cart.objects.get(id=request.session['cart'])
        except Cart.DoesNotExist:
            cart = None
    else:
        cart = Cart.objects.create()
        if cart:
            request.session['cart'] = cart.id
    return cart


# Get the object name (macaron set or collection) being added to the cart.
def get_object_name(item_type, object_instance):
    if item_type == 'macaronset':
        object_name = object_instance.macaron.name
    else:
        object_name = object_instance.name
    return object_name


# Remove cart item from cart
# Set the boolean for the CartItem to False
def remove_from_cart(request, slug):
    if request.method == "POST":
        # get cart ID from session
        cart = get_object_or_404(Cart, id=request.session.get('cart'))
        # grab the cart item that matches the cart session and slug provided
        cart_item = get_object_or_404(CartItem, cart=cart, slug=slug)
        cart_item.active = False
        cart_item.save()
        messages.add_message(request, messages.SUCCESS,
                             mark_safe(
                                 f"<i class='bi bi-cart-x'></i> &nbsp;{cart_item.content_object.get_name()} has been removed from your cart."))
        return redirect(reverse('cart:view'))
    else:
        return redirect(reverse('cart:view'))


# emtpy endpoint to ensure successful login of user with a GET endpoint
@login_required
def checkout_request(request):
    return redirect(reverse('cart:checkout_confirm'))


# verify order details, delete request.session cart storage and redirect to checkout complete endpoint
class Checkout(LoginRequiredMixin, View):
    template_name = 'cart/checkout_confirm.html'

    def get(self, request):
        cart = get_object_or_404(Cart, id=request.session.get('cart'))
        # check if order id is stored in request.session and get it if it exists.
        # if it doesn't exist, create a new order and store it in request.session
        if request.session.get('order_id'):
            order = get_object_or_404(Order, id=request.session.get('order_id'))
        else:
            order = Order.objects.create(
                user=request.user,
                cart=cart,
                code=random_string_generator('', 8)
            )
            request.session['order_id'] = order.id
        if order:
            order.total = order.calculate_total()
            order.save()
            messages.add_message(request, messages.INFO, "Please confirm your order details.")
            context = {
                'order': order,
                'GOOGLE_RECAPTCHA_SITE_KEY': settings.GOOGLE_RECAPTCHA_SITE_KEY,
            }
            return render(request, self.template_name, context)
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong. Please place your order again.")
            return redirect(reverse('cart:view'))

    def post(self, request):
        if request.session.get('order_id'):
            order = get_object_or_404(Order, id=request.session.get('order_id'))

            # get recaptcha response from form
            recaptcha_response = request.POST.get('g-recaptcha-response')
            recaptcha_response_url = 'https://www.google.com/recaptcha/api/siteverify'
            recaptcha_response_values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            recaptcha_data = urllib.parse.urlencode(recaptcha_response_values).encode()
            recaptcha_request = urllib.request.Request(recaptcha_response_url, data=recaptcha_data)
            recaptcha_response = urllib.request.urlopen(recaptcha_request)
            recaptcha_result = json.loads(recaptcha_response.read().decode())

            if recaptcha_result['success']:
                # edit the order to make it active
                order.active = True
                order.status = 'created'
                order.save()

                # send email
                context = {
                    'order': order,
                }
                html_message = render_to_string('orders/emails/order_confirmation.html', context)
                send_mail(
                    f"Macalicious Order Confirmation | Order: {order.code}",
                    strip_tags(html_message),
                    'Macalicious <shop.macalicious@gmail.com>',
                    [order.user.email, 'shop.macalicious@gmail.com'],
                    fail_silently=True,
                    html_message=html_message
                )
                messages.add_message(request, messages.SUCCESS,
                                     mark_safe(
                                         f"Your order has been placed.<br>Thank you for choosing <span class='fancy'>Macalicious!</span>, {order.user.first_name}!"))
                if request.session.get('cart'):
                    del request.session['cart']  # delete cart id stored in request.session
                if request.session.get('order_id'):
                    del request.session['order_id']
                return redirect(reverse('cart:checkout_complete', kwargs={'order_code': order.code}))
            else:
                messages.add_message(request, messages.ERROR, "Something went wrong. Please try again.")
                return redirect(reverse('cart:checkout_confirm'))
        else:
            messages.add_message(request, messages.ERROR, "POST: Something went wrong. Please place your order again.")
            return redirect(reverse('cart:view'))


# checkout complete endpoint
@login_required
def checkout_complete(request, order_code):
    template_name = 'cart/checkout_complete.html'
    order = get_object_or_404(Order, code=order_code)
    context = {
        'order': order,
    }
    return render(request, template_name, context)


# Cart view endpoint [url: /cart/] - Only GET Request
class CartPage(View):
    template_name = 'cart/view.html'

    def get(self, request):
        cart = get_or_create_cart(request)
        recommended_macaron_sets = MacaronSet.objects.recommended()
        context = {
            'cart': cart,
            'recommended_macaron_sets': recommended_macaron_sets,
        }
        return render(request, self.template_name, context)
