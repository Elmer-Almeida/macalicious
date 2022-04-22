import requests

from django.shortcuts import render, redirect
from django.views.generic import View
from registration.backends.default.views import RegistrationView
from registration.signals import user_registered

from shop.models import Set, Collection, CustomCollectionType
from .forms import RegistrationForm


# Landing/Home page endpoint [url: /]
class LandingPage(View):
    template_name = 'pages/landing.html'

    def get(self, request):
        featured_macaron_sets = Set.objects.featured()
        featured_macaron_collections = Collection.objects.featured()

        context = {
            'featured_macaron_sets': featured_macaron_sets,
            'featured_macaron_collections': featured_macaron_collections,
            'custom_collection_types': CustomCollectionType.objects.all(),
        }
        return render(request, self.template_name, context)


# TODO: finish about page content and design
# About page endpoint [url: /about/]
class AboutPage(View):
    template_name = 'pages/about.html'

    def get(self, request):
        context = {

        }
        return render(request, self.template_name, context)


# Terms of service page endpoint [url: /tos/]
class TOSPage(View):
    template_name = 'pages/tos.html'

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


######################################################################################
###################### Django Registration Redux Component ###########################
######################################################################################

# Custom registration view for user creation
# path: /accounts/register/
class CustomRegistrationView(RegistrationView):
    form_class = RegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('/')
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)


# Called via signals when user registers. Creates different profiles and associations
def user_created(sender, user, request, **kwargs):
    form = RegistrationForm(request.POST)
    # Update the first and last name for user
    user.first_name = form.data['first_name'].capitalize()
    user.last_name = form.data['last_name'].capitalize()
    user.save()


# call user_created signal after user registered to update first and last name
user_registered.connect(user_created)

######################################################################################
######################################################################################
######################################################################################
