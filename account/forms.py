from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit


class AccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email'
        ]

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        # required fields - username is also required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        self.fields['first_name'].widget.attrs.update({'autofocus': True})
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-6'),
                Column('last_name', css_class='form-group col-6'),
                css_class='form-row row mb-1'
            ),
            Row('username', css_class='mb-1'),
            Row('email', css_class='mb-1'),
            Submit('submit', 'Update Account', css_class='btn-primary')
        )

    def clean(self):
        errors = []  # keep track of validation errors

        username = self.cleaned_data['username']
        email = self.cleaned_data['email']

        # check if data entered exists in the database and is not the users data
        if User.objects.filter(username=username).exists() and username != self.user.username:
            self.fields['username'].widget.attrs['class'] = 'input-error'
            errors.append(ValidationError('That username is already taken.'))
        if User.objects.filter(email=email).exists() and email != self.user.email:
            self.fields['email'].widget.attrs['class'] = 'input-error'
            errors.append(ValidationError('That email address already belongs to an account.'))

        # if there are validation errors, raise them
        if errors:
            raise ValidationError(errors)

        return self.cleaned_data


# Password reset form
# update user password and confirm password correct
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row('old_password', css_class='mb-0'),
            Row('new_password1', css_class='mb-0'),
            Row('new_password2', css_class='mb-1'),
            Submit('submit', 'Update Password')
        )
