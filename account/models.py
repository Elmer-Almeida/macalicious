from django.db import models

from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = PhoneNumberField()
    about = models.TextField(max_length=5000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def admin_user_full_name(self):
        if self.user.get_full_name():
            return f"{self.user.get_full_name()}"
        else:
            return f"Not Specified"

    admin_user_full_name.short_description = "Full Name"

    def admin_user_email(self):
        return f"{self.user.email}"

    admin_user_email.short_description = "Email"
