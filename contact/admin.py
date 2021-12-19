from django.contrib import admin
from django.core.mail import send_mass_mail

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
    actions = [
        'contact_email_respond'
    ]

    @admin.action(description='Respond by email')
    def contact_email_respond(self, request, queryset):
        # get all emails to respond to
        recipient_list = [recipient for recipient in queryset]

        messages = [(
            f"{recipient.reason} - Contact | Macalicious",  # subject
            'This is the response',  # message
            "Macalicious <shop.macalicious@gmail.com>",  # from
            [recipient.email]  # to
        ) for recipient in recipient_list]

        send_mass_mail(messages, fail_silently=True)


admin.site.register(Contact, ContactAdmin)
