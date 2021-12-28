from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.conf import settings

from cart.forms import AddToCartForm

from .models import Set, Collection, Macaron, CustomCollection, CustomCollectionType


# Shop page endpoint [url: /shop/]
class ShopPage(View):
    template_name = 'shop/view.html'

    def get(self, request):
        macaron_sets = Set.objects.all()
        macaron_collections = Collection.objects.all()
        custom_collection_types = CustomCollectionType.objects.all()
        context = {
            'macaron_sets': macaron_sets,
            'macaron_collections': macaron_collections,
            'add_to_cart_form': AddToCartForm(),
            'custom_collection_types': custom_collection_types,
        }
        return render(request, self.template_name, context)


class SetDetailPage(View):
    template_name = 'shop/set_detail.html'

    def get(self, request, slug):
        macaron_set = get_object_or_404(Set, slug=slug)
        macaron_recommended_sets = Set.objects.recommended()
        context = {
            'macaron_set': macaron_set,
            'add_to_cart_form': AddToCartForm(),
            'macaron_recommended_sets': macaron_recommended_sets,
        }
        return render(request, self.template_name, context)


class CollectionDetailPage(View):
    template_name = 'shop/collection_detail.html'

    def get(self, request, slug):
        macaron_collection = get_object_or_404(Collection, slug=slug)
        macaron_recommended_collections = Collection.objects.recommended()
        context = {
            'macaron_collection': macaron_collection,
            'add_to_cart_form': AddToCartForm(),
            'macaron_recommended_collections': macaron_recommended_collections,
        }
        return render(request, self.template_name, context)


class CustomCollectionPage(LoginRequiredMixin, View):
    template_name = 'shop/custom_collection.html'

    def get(self, request, slug):
        custom_collection_type = get_object_or_404(CustomCollectionType, slug=slug)
        macaron_recommended_collections = Collection.objects.recommended()
        macaron_recommended_sets = Set.objects.recommended()
        macarons = Macaron.objects.all()
        context = {
            'macarons': macarons,
            'add_to_cart_form': AddToCartForm(),
            'custom_collection_type': custom_collection_type,
            'macaron_recommended_sets': macaron_recommended_sets,
            'macaron_recommended_collections': macaron_recommended_collections,
        }
        return render(request, self.template_name, context)
