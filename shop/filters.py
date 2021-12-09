from django.contrib import admin
from django.db.models import Q
from django.utils.html import mark_safe

from .models import MacaronCollection, MacaronCollectionItem


class TagListFilter(admin.SimpleListFilter):
    title = 'tag'
    parameter_name = 'tags__name'

    def lookups(self, request, model_admin):
        return (
            ('vegan', 'Vegan'),
            ('gluten-free', 'Gluten Free'),
            ('halal', 'Halal')
        )

    def queryset(self, request, queryset):
        if self.value() == 'vegan':
            return queryset.filter(
                Q(tags__name="Vegan")
            )
        if self.value() == 'gluten-free':
            return queryset.filter(
                Q(tags__name="Gluten Free")
            )
        if self.value() == 'halal':
            return queryset.filter(
                Q(tags__name="Halal")
            )


class OnSaleFilter(admin.SimpleListFilter):
    title = 'discount'
    parameter_name = 'sale_price'

    def lookups(self, request, model_admin):
        return (
            ('original', 'Original Price'),
            ('on-sale', 'Discounted Price')
        )

    def queryset(self, request, queryset):
        if self.value() == 'on-sale':
            return queryset.filter(
                Q(sale_price__gt=0)
            )
        if self.value() == 'original':
            return queryset.filter(
                Q(sale_price=0)
            )


class OriginalPriceRangeFilter(admin.SimpleListFilter):
    title = 'price'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('1.00 - 9.99', mark_safe('$1.00 &nbsp; to &nbsp; $9.99')),
            ('10.00 - 19.99', mark_safe('$10.00 &nbsp; to &nbsp; $19.99')),
            ('20.00 - 29.99', mark_safe('$20.00 &nbsp; to &nbsp; $29.99')),
            ('30.00 - 39.99', mark_safe('$30.00 &nbsp; to &nbsp; $39.99')),
            ('40.00 - 49.99', mark_safe('$40.00 &nbsp; to &nbsp; $49.99')),
            ('50.00+', '$50.00+')
        )

    def queryset(self, request, queryset):
        if self.value() == '1.00 - 9.99':
            return queryset.filter(
                (Q(price__gte=1.00) &
                 Q(price__lte=9.99)) |
                (Q(sale_price__gte=1.00) &
                 Q(sale_price__lte=9.99))
            )
        if self.value() == '10.00 - 19.99':
            return queryset.filter(
                (Q(price__gte=10.00) &
                 Q(price__lte=19.99)) |
                (Q(sale_price__gte=10.00) &
                 Q(sale_price__lte=19.99))
            )
        if self.value() == '20.00 - 29.99':
            return queryset.filter(
                (Q(price__gte=20.00) &
                 Q(price__lte=29.99)) |
                (Q(sale_price__gte=20.00) &
                 Q(sale_price__lte=29.99))
            )
        if self.value() == '30.00 - 39.99':
            return queryset.filter(
                (Q(price__gte=30.00) &
                 Q(price__lte=39.99)) |
                (Q(sale_price__gte=30.00) &
                 Q(sale_price__lte=39.99))
            )
        if self.value() == '40.00 - 49.99':
            return queryset.filter(
                (Q(price__gte=40.00) &
                 Q(price__lte=49.99)) |
                (Q(sale_price__gte=40.00) &
                 Q(sale_price__lte=49.99))
            )
        if self.value() == '50.00+':
            return queryset.filter(
                Q(price__gte=50.00) |
                Q(sale_price__gte=50.00)
            )


# for collection to filter by collection item
class CollectionItemFilter(admin.SimpleListFilter):
    title = 'macarons collection item'
    parameter_name = 'macarons__macaron'

    def lookups(self, request, model_admin):
        macarons = MacaronCollectionItem.objects.filter(active=True)
        macarons_list = []
        for item in macarons:
            macarons_list.append(
                (item.macaron.name + "-" + str(item.quantity),
                 item.macaron.name + '  (' + str(item.quantity) + ' macarons)')
            )
        return macarons_list

    def queryset(self, request, queryset):
        if self.value():
            macaron_name = self.value().split("-")[0]
            macaron_quantity = self.value().split("-")[1]
            return queryset.filter(
                Q(macarons__macaron__name=macaron_name) &
                Q(macarons__quantity=macaron_quantity)
            )


class CollectionFilter(admin.SimpleListFilter):
    title = 'collection'
    parameter_name = 'macaroncollection'

    def lookups(self, request, model_admin):
        collections = MacaronCollection.objects.all()
        collection_list = []
        for collection in collections:
            collection_list.append(
                (collection.name, collection.name)
            )
        return collection_list

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(
                Q(macaroncollection__name=self.value())
            )
