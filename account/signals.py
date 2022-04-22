from django.contrib.auth.signals import user_logged_out
from django.contrib.auth import get_user_model
from django.utils.html import mark_safe
from django.contrib import messages

from registration.signals import user_registered

from .models import Profile


User = get_user_model()


# create user profile when user registers for an account
def user_registered_receiver(sender, user, request, **kwargs):
    profile = Profile.objects.create(
        user=user,
        phone_number=request.POST.get('phone_number'),
    )
    profile.save()


user_registered.connect(user_registered_receiver)


# display message when user logs out of their account
def user_logged_out_receiver(sender, request, **kwargs):
    messages.add_message(request, messages.INFO, mark_safe('You have successfully logged out.&nbsp;&nbsp;<a href="/accounts/login/">Log back in</a>.'))


user_logged_out.connect(user_logged_out_receiver, sender=get_user_model())
