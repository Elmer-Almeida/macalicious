from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.db.models import Q

from shop.models import CustomCollectionType, CustomCollection


class ItemTypeFilter(admin.SimpleListFilter):
    title = 'item type'
    parameter_name = 'item_type'

    def lookups(self, request, model_admin):
        return (
            ('set', 'Macaron Set'),
            ('collection', 'Macaron Collection'),
            ('customcollection', 'Macaron Custom Collection')
        )

    def queryset(self, request, queryset):
        if self.value():
            try:
                item_type = ContentType.objects.get(model=self.value())
                return queryset.filter(
                    Q(item_type=item_type)
                )
            except ContentType.DoesNotExist:
                return queryset


class PriceRangeFilter(admin.SimpleListFilter):
    title = 'price range'
    parameter_name = 'total'

    def lookups(self, request, model_admin):
        return (
            ('1.00-19.99', '$1.00 to $19.99'),
            ('20.00-39.99', '$20.00 - $39.99'),
            ('40.00-59.99', '$40.00 - $59.99'),
            ('60.00-79.99', '$60.00 - $79.99'),
            ('80.00-99.99', '$80.00 - $99.99'),
            ('100+', '$100.00+')
        )

    def queryset(self, request, queryset):
        if self.value() == '1.00-19.99':
            return queryset.filter(
                Q(total__gte=1.00) &
                Q(total__lte=19.99)
            )
        if self.value() == '20.00-39.99':
            return queryset.filter(
                Q(total__gte=20.00) &
                Q(total__lte=39.99)
            )
        if self.value() == '40.00-59.99':
            return queryset.filter(
                Q(total__gte=40.00) &
                Q(total__lte=59.99)
            )
        if self.value() == '60.00-79.99':
            return queryset.filter(
                Q(total__gte=60.00) &
                Q(total__lte=79.99)
            )
        if self.value() == '80.00-99.99':
            return queryset.filter(
                Q(total__gte=80.00) &
                Q(total__lte=99.99)
            )
        if self.value() == '100+':
            return queryset.filter(
                Q(total__gte=100.00)
            )
