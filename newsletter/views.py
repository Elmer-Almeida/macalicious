import json
import urllib

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import View

from macalicious.utils import random_string_generator
from .forms import NewsletterForm, NewsletterShortForm
from .models import Newsletter


class NewsletterShortSignUp(View):

    def post(self, request):
        newsletter_form = NewsletterShortForm(data=request.POST)
        if newsletter_form.is_valid():
            # get recaptcha response from form
            recaptcha_response = request.POST.get('g-recaptcha-response')
            recaptcha_response_url = 'https://www.google.com/recaptcha/api/siteverify'
            recaptcha_response_values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            recaptcha_data = urllib.parse.urlencode(recaptcha_response_values).encode()
            recaptcha_request = urllib.request.Request(recaptcha_response_url, data=recaptcha_data)
            recaptcha_response = urllib.request.urlopen(recaptcha_request)
            recaptcha_result = json.loads(recaptcha_response.read().decode())

            if recaptcha_result['success']:
                newsletter = newsletter_form.save(commit=False)
                # create a large code to add to uniqueness - 18 characters + prefix: "newsletter_"
                code = random_string_generator("newsletter_", 18)
                newsletter.code = code
                newsletter.save()
                messages.add_message(request, messages.INFO, 'Let\'s get to know each other better.')
                return redirect(reverse('newsletter:signup', kwargs={'code': newsletter.code}))
            else:
                # recaptcha is invalid
                messages.add_message(request, messages.ERROR, 'Something went wrong. Please try again later.')
                return redirect(reverse('newsletter:signup'))
        else:
            # check if newsletter already exists
            newsletter_instance = Newsletter.objects.get(email=request.POST.get('email')).exists()
            if newsletter_instance:
                messages.add_message(request, messages.ERROR, 'You have already signed up for our newsletter.')
                return redirect(reverse('newsletter:signup'))
            else:
                # newsletter sign up form is invalid
                messages.add_message(request, messages.ERROR, 'Something went wrong. Please try again later.')
                return redirect(reverse('newsletter:signup'))


class NewsletterSignUp(View):
    template_name = "newsletter/signup.html"

    def get(self, request, code=''):
        context = {}
        if code:
            newsletter = get_object_or_404(Newsletter, code=code)
            newsletter_form = NewsletterForm(instance=newsletter)
            context['newsletter'] = newsletter
        else:
            newsletter_form = NewsletterForm()
        context['newsletter_form'] = newsletter_form
        return render(request, self.template_name, context)

    def post(self, request, code=''):
        if code:
            newsletter = get_object_or_404(Newsletter, code=code)
            newsletter_form = NewsletterForm(data=request.POST, instance=newsletter)
        else:
            newsletter_form = NewsletterForm(data=request.POST)
        if newsletter_form.is_valid():
            # get recaptcha response from form
            recaptcha_response = request.POST.get('g-recaptcha-response')
            recaptcha_response_url = 'https://www.google.com/recaptcha/api/siteverify'
            recaptcha_response_values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            recaptcha_data = urllib.parse.urlencode(recaptcha_response_values).encode()
            recaptcha_request = urllib.request.Request(recaptcha_response_url, data=recaptcha_data)
            recaptcha_response = urllib.request.urlopen(recaptcha_request)
            recaptcha_result = json.loads(recaptcha_response.read().decode())

            if recaptcha_result['success']:
                newsletter_instance = newsletter_form.save()

                # send email confirmation
                context = {
                    'newsletter': newsletter_instance,
                }
                html_message = render_to_string('newsletter/emails/signup_confirmation.html', context)
                send_mail(
                    'Newsletter Signup | Macalicious',
                    strip_tags(html_message),
                    'Macalicious <shop.macalicious@gmail.com>',
                    [newsletter_instance.email, 'shop.macalicious@gmail.com'],
                    fail_silently=True,
                    html_message=html_message
                )
                messages.add_message(request, messages.SUCCESS, 'You have been added to our newsletter.')
                return redirect(reverse('newsletter:signup'))
            else:
                # recaptcha is not valid
                messages.add_message(request, messages.ERROR, 'Something went wrong. Please try again later.')
                if len(code) > 0:
                    return redirect(reverse('newsletter:signup', kwargs={'code': code}))
                else:
                    return redirect(reverse('newsletter:signup'))
        else:
            # newsletter signup form is not valid
            messages.add_message(request, messages.ERROR, 'Something went wrong. Please try again later.')
            if len(code) > 0:
                return redirect(reverse('newsletter:signup', kwargs={'code': code}))
            else:
                return redirect(reverse('newsletter:signup'))


# newsletter unsubscribe [url: /newsletter/unsubscribe/<code>/]
def newsletter_unsubscribe(request, code):
    if request.method == "GET":
        newsletter_instance = get_object_or_404(Newsletter, code=code)
        newsletter_instance.active = False
        newsletter_instance.save()
        messages.add_message(request, messages.SUCCESS, 'You have successfully unsubscribed from our newsletter.')
        return redirect(reverse('newsletter:signup'))
