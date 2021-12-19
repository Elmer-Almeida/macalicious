from django.shortcuts import render, redirect
from django.template import RequestContext
from django.views.generic import View
from registration.backends.default.views import RegistrationView
from registration.signals import user_registered

from shop.models import MacaronSet, MacaronCollection
from .forms import RegistrationForm


# Landing/Home page endpoint [url: /]
class LandingPage(View):
    template_name = 'pages/landing.html'

    def get(self, request):
        # TODO: redirecting to /shop/ for temporary measures
        # return redirect(reverse('shop:view'))

        # Remove cart and order_id session if it exists
        # if request.session.get('cart'):
        #     del request.session['cart']
        # if request.session.get('order_id'):
        #     del request.session['order_id']

        featured_macaron_sets = MacaronSet.objects.featured()
        featured_macaron_collections = MacaronCollection.objects.featured()

        context = {
            'featured_macaron_sets': featured_macaron_sets,
            'featured_macaron_collections': featured_macaron_collections,
        }
        return render(request, self.template_name, context)


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


#######################################################################################
############################# Error Page Views ########################################
#######################################################################################

# 400 error - Bad Request
def bad_request(request, exception):
    context = {
        'context_instance': RequestContext(request)
    }
    render(request, '400.html', context, status=400)


# 403 error - Permission Denied
def permission_denied(request, exception):
    context = {
        'context_instance': RequestContext(request)
    }
    render(request, '403.html', context, status=403)


# 404 error - Page not found
def page_not_found(request, exception):
    context = {
        'context_instance': RequestContext(request)
    }
    render(request, '404.html', context, status=404)


# 500 error - Server Error
def server_error(request):
    context = {
        'context_instance': RequestContext(request)
    }
    render(request, '500.html', context, status=500)


######################################################################################
######################################################################################
######################################################################################

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
