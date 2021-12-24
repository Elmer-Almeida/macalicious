from django.shortcuts import render

from shop.models import Set, Collection

from .forms import SearchForm


# search form endpoint [url: /search/?q=<query>]
def search_results(request):
    template_name = 'search/results.html'
    query = request.GET.get('query')
    # Check all macaron sets for search query (name & description)
    macaron_set_results = Set.objects.search(query)
    # Check all collections for search query
    collection_results = Collection.objects.search(query)
    # add the form with the initial value (request.GET.query)
    search_form = SearchForm(initial=request.GET)
    context = {
        'query': query,
        'search_form': search_form,
        'macaron_set_results': macaron_set_results,
        'collection_results': collection_results,
    }
    return render(request, template_name, context)
