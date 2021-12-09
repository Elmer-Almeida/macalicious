from django.urls import path

from .views import AccountPage, PasswordChange


app_name = 'account'

urlpatterns = [
    path('', AccountPage.as_view(), name="view"),
    path('password-change/', PasswordChange.as_view(), name="password_change"),
]
