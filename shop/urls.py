from django.urls import path

from .views import ShopPage, SetDetailPage, CollectionDetailPage


app_name = 'shop'

urlpatterns = [
    path('', ShopPage.as_view(), name="view"),
    path('set/<slug>/', SetDetailPage.as_view(), name="set_detail"),
    path('collection/<slug>/', CollectionDetailPage.as_view(), name="collection_detail"),
]