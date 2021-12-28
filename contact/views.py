from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.template.loader import render_to_string
from django.utils.html import mark_safe, strip_tags
from django.views.generic import View

from macalicious.utils import handle_recaptcha_response
from .forms import ContactForm


# Contact page endpoint [url: /contact/]
class ContactPage(View):
    template_name = 'contact/view.html'

    def get(self, request):
        contact_form = ContactForm()
        if request.GET.get('reason').lower() == 'custom-order':
            data = {
                'reason': 'custom-order',
            }
            contact_form = ContactForm(initial=data)
        context = {
            'contact_form': contact_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            # get recaptcha response from form
            recaptcha_result = handle_recaptcha_response(request)

            if recaptcha_result['success']:
                contact_instance = contact_form.save(commit=False)
                if request.user.is_authenticated:
                    contact_instance.user = request.user
                contact_instance.save()
                # send email
                send_contact_request_email(contact_instance)
                messages.add_message(request, messages.SUCCESS,
                                     mark_safe('Your message has been sent! <br>We will get back to you shortly.'))
                return redirect(reverse("contact:view"))
            else:
                messages.error(request, messages.ERROR, 'Captcha input was wrong. Please try again.')
                return redirect(reverse("contact:view"))
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong. Please try again later.")
            return redirect(reverse("contact:view"))


def send_contact_request_email(contact_instance):
    context = {
        'contact': contact_instance
    }
    html_message = render_to_string('contact/emails/contact_request.html', context)
    send_mail(
        f"Contact | Reason: {contact_instance.reason} | Macalicious",
        strip_tags(html_message),
        "Macalicious <shop.macalicious@gmail.com>",
        ['shop.macalicious@gmail.com'],
        fail_silently=True,
        html_message=html_message
    )
