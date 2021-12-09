from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import Order


# View orders placed endpoint [url: /orders/]
class OrdersPage(LoginRequiredMixin, View):
    template_name = 'orders/view.html'

    def get(self, request):
        orders = Order.objects.active().filter(user=request.user).order_by('-created_at')
        context = {
            'orders': orders,
        }
        return render(request, self.template_name, context)
