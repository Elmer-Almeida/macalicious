from django.urls import path

from .views import NewsletterShortSignUp, NewsletterSignUp


app_name = "newsletter"

urlpatterns = [
    path('short/', NewsletterShortSignUp.as_view(), name="signup_short"),
    path('<code>/', NewsletterSignUp.as_view(), name="signup"),
    path('', NewsletterSignUp.as_view(), name="signup"),
]
