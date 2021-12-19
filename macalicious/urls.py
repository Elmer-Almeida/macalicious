from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.utils.html import mark_safe

from shop.sitemap import MacaronSetSitemap, MacaronCollectionSitemap
from .sitemap import StaticViewSitemap
from .views import LandingPage, TOSPage, CustomRegistrationView

sitemaps = {
    'static': StaticViewSitemap,
    'macaron_sets': MacaronSetSitemap,
    'macaron_collections': MacaronCollectionSitemap,
}

urlpatterns = [
                  path('admin/', admin.site.urls),  # admin panel endpoint

                  path('', LandingPage.as_view(), name="landing"),

                  # TODO: Removed about for temporary deployment
                  # path('about/', AboutPage.as_view(), name="about"),

                  path('tos/', TOSPage.as_view(), name="tos"),

                  path('contact/', include('contact.urls')),  # contact app endpoint
                  path('shop/', include('shop.urls')),  # shop app endpoint
                  path('newsletter/', include('newsletter.urls')),  # newsletter app endpoint
                  path('cart/', include('cart.urls')),  # cart app endpoint
                  path('orders/', include('orders.urls')),  # orders app endpoint
                  path('account/', include('account.urls')),
                  path('search/', include('search.urls')),

                  # account urls
                  path('accounts/register/', CustomRegistrationView.as_view(), name='registration_register'),
                  path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name="login"),
                  path('accounts/', include('registration.backends.default.urls')),

                  # sitemap
                  path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name="sitemap"),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = mark_safe(f"<b>Macalicious Admin</b>")
admin.site.site_title = mark_safe(f"Macalicious Admin Portal")
admin.site.index_title = mark_safe(f"Welcome to Macalicious Admin")
