from django.urls import path

from .views import ContactPage

app_name = 'contact'

urlpatterns = [
    path('', ContactPage.as_view(), name="view"),
]
