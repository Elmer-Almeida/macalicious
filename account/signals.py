from django.contrib.auth.models import User

from registration.signals import user_registered

from .models import Profile


def user_registered_receiver(sender, user, request, **kwargs):
    profile = Profile.objects.create(
        user=user,
        phone_number=request.POST.get('phone_number'),
    )
    profile.save()


user_registered.connect(user_registered_receiver)
