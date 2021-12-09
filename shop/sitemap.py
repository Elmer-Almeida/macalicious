from django.contrib.sitemaps import Sitemap

from shop.models import MacaronSet, MacaronCollection


class MacaronSetSitemap(Sitemap):
    changefreq = 'always'
    priority = 0.8

    def items(self):
        return MacaronSet.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, item):
        return item.get_absolute_url()


class MacaronCollectionSitemap(Sitemap):
    changefreq = 'always'
    priority = 0.8

    def items(self):
        return MacaronCollection.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, item):
        return item.get_absolute_url()
