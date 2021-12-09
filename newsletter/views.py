from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic import View
from django.contrib import messages

from macalicious.utils import random_string_generator

from .forms import NewsletterForm, NewsletterShortForm
from .models import Newsletter


class NewsletterShortSignUp(View):

    def post(self, request):
        newsletter_form = NewsletterShortForm(data=request.POST)
        if newsletter_form.is_valid():
            newsletter = newsletter_form.save(commit=False)
            code = random_string_generator("newsletter_")
            newsletter.code = code
            newsletter.save()
            messages.add_message(request, messages.INFO, 'Let\'s get to know each other better.')
            return redirect(reverse('newsletter:signup', kwargs={'code': newsletter.code}))


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
            newsletter_form.save()
            messages.add_message(request, messages.SUCCESS, 'You have been added to our newsletter.')
            return redirect(reverse('newsletter:signup'))
