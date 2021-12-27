from django.contrib import admin

from .filters import TagListFilter, OnSaleFilter, \
    OriginalPriceRangeFilter, CollectionItemFilter, CollectionFilter
from .models import Tag, Macaron, Image, Set, \
    CollectionItem, Collection, CollectionImage, \
    CustomCollectionType, CustomCollection


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


class ImageAdmin(admin.TabularInline):
    model = Image
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
        ImageAdmin
    ]


admin.site.register(Macaron, MacaronAdmin)


class SetAdmin(admin.ModelAdmin):
    list_editable = [
        'price', 'active', 'featured', 'order'
    ]
    list_display = [
        'get_name', 'quantity', 'price', 'admin_sale_price', 'active', 'featured', 'order',
        'admin_get_total', 'slug'
    ]
    raw_id_fields = [
        'macaron'
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


admin.site.register(Set, SetAdmin)


class CollectionItemAdmin(admin.ModelAdmin):
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


admin.site.register(CollectionItem, CollectionItemAdmin)


class CollectionImageAdmin(admin.TabularInline):
    model = CollectionImage
    fields = [
        'picture', 'caption', 'alt_text', 'active', 'featured'
    ]
    extra = 3


class CollectionAdmin(admin.ModelAdmin):
    list_editable = [
        'active', 'featured', 'order'
    ]
    list_display = [
        'name', 'get_macaron_list', 'price', 'admin_sale_price', 'active', 'featured', 'order', 'admin_get_total',
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
        CollectionImageAdmin
    ]


admin.site.register(Collection, CollectionAdmin)


class CustomCollectionTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'quantity_each', 'quantity_total', 'price', 'admin_sale_price', 'active', 'admin_get_total', 'slug', 'created_at', 'updated_at'
    ]
    list_editable = [
        'active', 'quantity_each', 'quantity_total'
    ]
    list_filter = [
        'quantity_total', 'active'
    ]
    readonly_fields = [
        'slug', 'created_at', 'updated_at'
    ]
    search_fields = [
        'name', 'description'
    ]


admin.site.register(CustomCollectionType, CustomCollectionTypeAdmin)


class CustomCollectionAdmin(admin.ModelAdmin):
    list_display = [
        '__str__', 'user', 'admin_get_macarons_list', 'slug', 'active', 'created_at', 'updated_at'
    ]
    list_filter = [
        'active'
    ]
    list_editable = [
        'active'
    ]
    raw_id_fields = [
        'user'
    ]
    readonly_fields = [
        'slug'
    ]
    search_fields = [
        'user__first_name', 'user__last_name', 'user__username', 'user__email',
        'macarons', 'slug', 'created_at', 'updated_at'
    ]


admin.site.register(CustomCollection, CustomCollectionAdmin)
