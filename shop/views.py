from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from cart.forms import AddToCartForm

from .models import MacaronSet, MacaronCollection


# Shop page endpoint [url: /shop/]
class ShopPage(View):
    template_name = 'shop/view.html'

    def get(self, request):
        macaron_sets = MacaronSet.objects.all()
        macaron_collections = MacaronCollection.objects.all()
        context = {
            'macaron_sets': macaron_sets,
            'macaron_collections': macaron_collections,
            'add_to_cart_form': AddToCartForm(),
        }
        return render(request, self.template_name, context)


class SetDetailPage(View):
    template_name = 'shop/set_detail.html'

    def get(self, request, slug):
        macaron_set = get_object_or_404(MacaronSet, slug=slug)
        macaron_recommended_sets = MacaronSet.objects.recommended()
        context = {
            'macaron_set': macaron_set,
            'add_to_cart_form': AddToCartForm(),
            'macaron_recommended_sets': macaron_recommended_sets,
        }
        return render(request, self.template_name, context)


class CollectionDetailPage(View):
    template_name = 'shop/collection_detail.html'

    def get(self, request, slug):
        macaron_collection = get_object_or_404(MacaronCollection, slug=slug)
        macaron_recommended_collections = MacaronCollection.objects.recommended()
        context = {
            'macaron_collection': macaron_collection,
            'add_to_cart_form': AddToCartForm(),
            'macaron_recommended_collections': macaron_recommended_collections,
        }
        return render(request, self.template_name, context)
