from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView

from .forms import AccountForm, CustomPasswordChangeForm


class AccountPage(View):
    template_name = 'account/view.html'

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        account_form = AccountForm(user=request.user, instance=user)
        context = {
            'account_form': account_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user = get_object_or_404(User, username=request.user.username)
        account_form = AccountForm(user=request.user, instance=user, data=request.POST)
        if account_form.is_valid():
            account_form.save()
            messages.add_message(request, messages.SUCCESS, "Your account has been updated.")
            return redirect(reverse('account:view'))
        else:
            messages.add_message(request, messages.ERROR, "Something went wrong. Please try again later.")


# Update a user's password with a new password
# Password constraints will still be the same
class PasswordChange(SuccessMessageMixin, PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url = 'account/password_change.html'
    success_message = "Your Password has been updated."
    form_class = CustomPasswordChangeForm
