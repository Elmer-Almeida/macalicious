import json
import urllib

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.utils.html import mark_safe, strip_tags
from django.views.generic import View

from .forms import ContactForm


# Contact page endpoint [url: /contact/]
class ContactPage(View):
    template_name = 'contact/view.html'

    def get(self, request):
        context = {
            'contact_form': ContactForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
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
                contact_instance = contact_form.save(commit=False)
                if request.user.is_authenticated:
                    contact_instance.user = request.user
                contact_instance.save()
                # send email
                context = {
                    'contact': contact_instance
                }
                html_message = render_to_string('contact/emails/contact_request.html', context)
                send_mail(
                    f"Contact | Reason: {contact_instance.reason} | Macalicious",
                    strip_tags(html_message),
                    "Macalicious <shop.macalicious@gmail.com>",
                    [contact_instance.email, 'shop.macalicious@gmail.com'],
                    fail_silently=True,
                    html_message=html_message
                )
                messages.add_message(request, messages.SUCCESS,
                                     mark_safe('Your message has been sent! <br>We will get back to you shortly.'))
                return redirect(reverse("contact:view"))
            else:
                messages.error(request, messages.ERROR, 'Captcha input was wrong. Please try again.')
                return redirect(reverse("contact:view"))
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong. Please try again later.")
            return redirect(reverse("contact:view"))
