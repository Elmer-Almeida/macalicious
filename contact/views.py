from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views.generic import View
from django.utils.html import mark_safe

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
            contact_instance = contact_form.save(commit=False)
            if request.user.is_authenticated:
                contact_instance.user = request.user
            contact_instance.save()
            messages.add_message(request, messages.SUCCESS,
                                 mark_safe('Your message has been sent! <br>We will get back to you shortly.'))
            return redirect(reverse("contact:view"))
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong. Please try again later.")
            return redirect(reverse("contact:view"))
