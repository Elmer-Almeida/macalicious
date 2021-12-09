from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View

from shop.models import MacaronSet, MacaronCollection


class Search(View):
    template_name = 'search/results.html'

    def get(self, request):
        search_query = request.GET.get('search_query')
        # Check all macaron sets for search query (name & description)
        macaron_set_results = MacaronSet.objects.filter(
            Q(macaron__name__icontains=search_query) |
            Q(macaron__description__icontains=search_query)
        )
        # Check all collections for search query
        collection_results = MacaronCollection.objects.filter(
            Q(macarons__macaron__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
        context = {
            'search_query': search_query,
            'macaron_set_results': macaron_set_results,
            'collection_results': collection_results,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        pass
