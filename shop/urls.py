from django.urls import path

from .views import ShopPage, SetsPage, CollectionsPage, SetDetailPage, CollectionDetailPage, CustomCollectionPage


app_name = 'shop'

urlpatterns = [
    path('', ShopPage.as_view(), name="view"),
    path('macarons/', SetsPage.as_view(), name="sets"),
    path('collections/', CollectionsPage.as_view(), name="collections"),
    path('set/<slug>/', SetDetailPage.as_view(), name="set_detail"),
    path('collection/<slug>/', CollectionDetailPage.as_view(), name="collection_detail"),

    # create custom collection
    path('collection/create/<slug>/', CustomCollectionPage.as_view(), name='custom_collection'),
]