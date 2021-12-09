from django import forms
from django.utils.html import mark_safe

from phonenumber_field.formfields import PhoneNumberField
from registration.forms import RegistrationFormTermsOfService, RegistrationFormUniqueEmail
from crispy_forms.layout import Layout, Column, Row, Submit, HTML
from crispy_forms.helper import FormHelper


# Custom user registration form with terms of service and unique email constraint
class RegistrationForm(RegistrationFormTermsOfService, RegistrationFormUniqueEmail):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    phone_number = PhoneNumberField(help_text='We will use this number to coordinate your order delivery.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].label = "Email Address"
        self.fields['tos'].label = mark_safe("I have read and agree to the <a href='/tos' target='_blank'>"
                                             "Terms of Service</a>.")
        self.fields['first_name'].widget.attrs.update({'autofocus': True})
        self.fields['username'].widget.attrs.update({'autofocus': False})

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-6'),
                Column('last_name', css_class='form-group col-6'),
                css_class='form-row row mb-0'
            ),
            Row('username', css_class='mb-0'),
            Row('email', css_class='mb-0'),
            Row('phone_number', css_class='mb-0'),
            Row('password1', css_class='mb-0'),
            Row('password2', css_class='mb-0'),
            Row('tos', css_class='mb-0'),
            HTML("<button type='submit' class='btn btn-primary'>"
                 "Create Account &nbsp;<i class='bi bi-arrow-right'></i>"
                 "</button>")
        )

    # clean first name
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        return first_name.capitalize()

    # clean last name
    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        return last_name.capitalize()

    # clean email
    def clean_email(self):
        email = self.cleaned_data['email']
        return email.lower()

    # clean username
    def clean_username(self):
        username = self.cleaned_data['username']
        return username.lower()
