from django.contrib import admin

from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'get_full_name', 'email', 'user', 'reason', 'created_at', 'updated_at'
    ]
    list_filter = [
        'reason'
    ]
    list_editable = [
        'reason'
    ]
    readonly_fields = [
        'first_name', 'last_name', 'email', 'message', 'created_at', 'updated_at'
    ]
    search_fields = [
        'first_name', 'last_name', 'email', 'message', 'reason',
        'user__username', 'user__first_name', 'user__last_name', 'user__email'
    ]


admin.site.register(Contact, ContactAdmin)
