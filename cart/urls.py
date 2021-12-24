from django.urls import path

from .views import CartPage, add_to_cart, remove_from_cart, \
    checkout_request, Checkout, checkout_complete

app_name = 'cart'

urlpatterns = [
    path('', CartPage.as_view(), name="view"),
    path('add/<slug>/', add_to_cart, name="add_to_cart"),
    path('remove/<slug>/', remove_from_cart, name="remove_from_cart"),

    path('checkout/', checkout_request, name="checkout_request"),
    path('checkout/confirm/', Checkout.as_view(), name="checkout_confirm"),
    path('checkout/complete/<order_code>/', checkout_complete, name="checkout_complete"),
]