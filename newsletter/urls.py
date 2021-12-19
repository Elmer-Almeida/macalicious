from django.urls import path

from .views import NewsletterShortSignUp, NewsletterSignUp, newsletter_unsubscribe

app_name = "newsletter"

urlpatterns = [
    path('short/', NewsletterShortSignUp.as_view(), name="signup_short"),
    path('unsubscribe/<code>/', newsletter_unsubscribe, name="unsubscribe"),
    path('<code>/', NewsletterSignUp.as_view(), name="signup"),
    path('', NewsletterSignUp.as_view(), name="signup"),
]
