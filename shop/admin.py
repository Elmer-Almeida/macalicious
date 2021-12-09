from django.contrib import admin

from .filters import TagListFilter, OnSaleFilter,\
    OriginalPriceRangeFilter, CollectionItemFilter, CollectionFilter
from .models import Tag, Macaron, MacaronImage, MacaronSet,\
    MacaronCollectionItem, MacaronCollection, MacaronCollectionImage


class TagAdmin(admin.ModelAdmin):
    list_editable = [
        'active'
    ]
    list_display = [
        'name', 'slug', 'active', 'created_at', 'updated_at'
    ]
    list_filter = [
        'active'
    ]
    readonly_fields = [
        'created_at', 'updated_at'
    ]
    search_fields = [
        'name'
    ]


admin.site.register(Tag, TagAdmin)


class MacaronImageAdmin(admin.TabularInline):
    model = MacaronImage
    fields = [
        'picture', 'caption', 'alt_text', 'active', 'featured'
    ]
    extra = 3


class MacaronAdmin(admin.ModelAdmin):
    list_editable = [
        'active'
    ]
    list_display = [
        'name', 'get_macaron_tags', 'slug', 'active', 'created_at', 'updated_at'
    ]
    list_filter = [
        'active', TagListFilter
    ]
    readonly_fields = [
        'slug', 'created_at', 'updated_at'
    ]
    search_fields = [
        'tags__name', 'name', 'description'
    ]
    inlines = [
        MacaronImageAdmin
    ]


admin.site.register(Macaron, MacaronAdmin)


class MacaronSetAdmin(admin.ModelAdmin):
    list_editable = [
        'active', 'featured'
    ]
    list_display = [
        'get_name', 'quantity', 'admin_get_price', 'admin_sale_price', 'active', 'featured', 'admin_get_total',
        'slug', 'created_at', 'updated_at'
    ]
    list_filter = [
        'active', OnSaleFilter
    ]
    readonly_fields = [
        'admin_get_total', 'slug', 'created_at', 'updated_at'
    ]
    search_fields = [
        'macaron__name',
    ]


admin.site.register(MacaronSet, MacaronSetAdmin)


class MacaronCollectionItemAdmin(admin.ModelAdmin):
    list_editable = [
        'active'
    ]
    list_display = [
        '__str__', 'quantity', 'admin_collection_list', 'active', 'created_at', 'updated_at'
    ]
    list_filter = [
        'active', CollectionFilter
    ]
    readonly_fields = [
        'admin_collection_list', 'created_at', 'updated_at'
    ]
    search_fields = [
        'macaroncollection__name', 'macaron__name'
    ]


admin.site.register(MacaronCollectionItem, MacaronCollectionItemAdmin)


class MacaronCollectionImageAdmin(admin.TabularInline):
    model = MacaronCollectionImage
    fields = [
        'picture', 'caption', 'alt_text', 'active', 'featured'
    ]
    extra = 3


class MacaronCollectionAdmin(admin.ModelAdmin):
    list_editable = [
        'active', 'featured'
    ]
    list_display = [
        'name', 'get_macaron_list', 'price', 'admin_sale_price', 'active', 'featured', 'admin_get_total',
        'slug', 'created_at', 'updated_at'
    ]
    list_filter = [
        'active', OnSaleFilter, OriginalPriceRangeFilter, CollectionItemFilter
    ]
    readonly_fields = [
        'slug', 'created_at', 'updated_at'
    ]
    search_fields = [
        'macarons__macaron__name', 'name'
    ]
    inlines = [
        MacaronCollectionImageAdmin
    ]


admin.site.register(MacaronCollection, MacaronCollectionAdmin)
