from django.urls import path

from.views import OrdersPage


app_name = 'orders'

urlpatterns = [
    path('', OrdersPage.as_view(), name="view"),
]