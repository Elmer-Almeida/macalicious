from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import View
from django.shortcuts import render

from .models import Order


# View orders placed endpoint [url: /orders/]
class OrdersPage(LoginRequiredMixin, View):
    template_name = 'orders/view.html'

    def get(self, request):
        all_orders = Order.objects.active().filter(user=request.user)
        pagination = Paginator(all_orders, 5)

        page_number = request.GET.get('page')
        orders = pagination.get_page(page_number)

        context = {
            'orders': orders,
            'pagination_object': pagination,
        }
        return render(request, self.template_name, context)
