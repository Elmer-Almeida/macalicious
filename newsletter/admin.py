from django.contrib import admin

from .models import Newsletter


class NewsletterAdmin(admin.ModelAdmin):
    fields = [
        "__all__"
    ]
    list_display = [
        'first_name', 'last_name', 'email', 'active', 'created_at', 'updated_at'
    ]
    list_filter = [
        'active'
    ]
    list_editable = [
        'active'
    ]
    readonly_fields = [
        'code', 'created_at', 'updated_at'
    ]


admin.site.register(Newsletter, NewsletterAdmin)
