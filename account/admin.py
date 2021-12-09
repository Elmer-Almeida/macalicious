from django.shortcuts import reverse
from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        '__str__', 'admin_user_full_name', 'user', 'admin_user_email', 'phone_number'
    ]
    search_fields = [
        'user__username', 'user__first_name', 'user__last_name', 'user__email', 'phone_number'
    ]
    readonly_fields = [
        'admin_user_full_name', 'user', 'admin_user_email', 'phone_number', 'about'
    ]


admin.site.register(Profile, ProfileAdmin)
