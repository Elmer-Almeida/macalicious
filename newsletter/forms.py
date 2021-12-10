from django import forms
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Submit, Button

from .models import Newsletter


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = [
            'first_name', 'last_name', 'email'
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
            HTML('<div class="g-recaptcha mb-3" data-sitekey="' + settings.GOOGLE_RECAPTCHA_SITE_KEY + '"></div>'),
            Submit('submit', 'Sign Up', css_class='btn-primary'),
            Button('cancel', "Go Back", css_class='btn', onclick="javascript:location.href = '/';")
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


class NewsletterShortForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = [
            'email'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row('email', css_class='mb-1'),
            HTML('<div class="g-recaptcha mb-3" data-sitekey="' + settings.GOOGLE_RECAPTCHA_SITE_KEY + '"></div>'),
            Submit('submit', 'Sign Up', css_class='btn-primary')
        )

    def clean_email(self):
        first_name = self.cleaned_data['email']
        return first_name.lower()
