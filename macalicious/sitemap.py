from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    changefreq = 'always'
    priority = 0.6

    def items(self):
        # TODO: removed landing and about for temporary deployment purposes
        # return ['landing', 'about', 'tos']
        return [
            'landing', 'tos', 'shop:view', 'auth_login', 'registration_register', 'orders:view', 'cart:view'
        ]

    def location(self, item):
        return reverse(item)
