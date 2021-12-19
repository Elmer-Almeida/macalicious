from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from django import forms
from django.conf import settings

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name', 'email', 'reason', 'message'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'autofocus': True})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-6'),
                Column('last_name', css_class='form-group col-6'),
                css_class='form-row row mb-1'
            ),
            Row('email', css_class='mb-1'),
            Row('reason', css_class='mb-1'),
            Row('message', css_class='mb-1'),
            HTML('<div class="g-recaptcha mb-3" data-sitekey="' + settings.GOOGLE_RECAPTCHA_SITE_KEY + '"></div>'),
            HTML(
                '<button type="submit" class="btn btn-primary">'
                'Send Message &nbsp;<i class="bi bi-arrow-right"></i>'
                '</button>'
            )
        )

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name.capitalize()

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()

    def clean_concern(self):
        concern = self.cleaned_data['concern']
        return concern.lower()

    def clean_message(self):
        message = self.cleaned_data['message']
        return message
