from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import View

from macalicious.utils import random_string_generator, handle_recaptcha_response
from .forms import NewsletterForm, NewsletterShortForm
from .models import Newsletter


class NewsletterShortSignUp(View):

    def get(self, request):
        return redirect(reverse("newsletter:signup"))

    def post(self, request):
        newsletter_form = NewsletterShortForm(data=request.POST)
        if newsletter_form.is_valid():
            # get recaptcha response from form
            recaptcha_result = handle_recaptcha_response(request)

            if recaptcha_result['success']:
                newsletter_instance = newsletter_form.save(commit=False)
                # create a large code to add to uniqueness - 18 characters + prefix: "newsletter_"
                code = random_string_generator("newsletter_", 18)
                newsletter_instance.code = code
                newsletter_instance.save()
                # send email confirmation -- send email to admin too
                send_newsletter_confirmation_email(newsletter_instance)
                messages.add_message(request, messages.INFO, 'Let\'s get to know each other better.')
                return redirect(reverse('newsletter:signup', kwargs={'code': newsletter_instance.code}))
            else:
                # recaptcha is invalid
                messages.add_message(request, messages.ERROR, 'Please provide a valid captcha response.')
                return redirect("%s?email=%s" % (reverse("newsletter:signup"), request.POST.get('email')))
        else:
            # check if newsletter already exists
            if check_newsletter_instance_exist(request, request.POST.get("email")):
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
            if request.GET.get('email'):
                newsletter_form = NewsletterForm(initial={'email': request.GET.get('email')})
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
            recaptcha_result = handle_recaptcha_response(request)

            if recaptcha_result['success']:
                newsletter_instance = newsletter_form.save(commit=False)
                if not newsletter_instance.code:
                    newsletter_instance.code = random_string_generator("newsletter_", 18)
                newsletter_instance.save()

                # send email confirmation
                send_newsletter_confirmation_email(newsletter_instance)
                messages.add_message(request, messages.SUCCESS, 'You have been added to our newsletter.')
                return redirect(reverse('newsletter:signup'))
            else:
                # recaptcha is not valid
                messages.add_message(request, messages.ERROR, 'Please provide a valid captcha response.')
                if len(code) > 0:
                    return redirect(reverse('newsletter:signup', kwargs={'code': code}))
                else:
                    return redirect(reverse('newsletter:signup'))
        else:
            # newsletter signup form is not valid
            if check_newsletter_instance_exist(request, request.POST.get('email')):
                return redirect(reverse('newsletter:signup'))
            else:
                messages.add_message(request, messages.ERROR, 'Something went wrong. Please try again later.')
                if len(code) > 0:
                    return redirect(reverse('newsletter:signup', kwargs={'code': code}))
                else:
                    return redirect(reverse('newsletter:signup'))


def check_newsletter_instance_exist(request, newsletter_email):
    email_check = Newsletter.objects.filter(email=newsletter_email.lower())
    messages.add_message(request, messages.ERROR, "You have already signed up for our newsletter.")
    if email_check:
        return True
    return False


def send_newsletter_confirmation_email(newsletter_instance):
    context = {
        'newsletter': newsletter_instance,
    }
    html_message = render_to_string('newsletter/emails/signup_confirmation.html', context)
    send_mail(
        'Newsletter Signup Confirmation | Macalicious',
        strip_tags(html_message),
        'Macalicious <shop.macalicious@gmail.com>',
        [newsletter_instance.email, 'shop.macalicious@gmail.com'],
        fail_silently=True,
        html_message=html_message
    )


# newsletter unsubscribe [url: /newsletter/unsubscribe/<code>/]
def newsletter_unsubscribe(request, code):
    if request.method == "GET":
        newsletter_instance = get_object_or_404(Newsletter, code=code)
        newsletter_instance.active = False
        newsletter_instance.save()
        messages.add_message(request, messages.SUCCESS, 'You have successfully unsubscribed from our newsletter.')
        return redirect(reverse('newsletter:signup'))
