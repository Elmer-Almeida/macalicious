from django.contrib.sitemaps import Sitemap

from shop.models import Set, Collection


class MacaronSetSitemap(Sitemap):
    changefreq = 'always'
    priority = 0.8

    def items(self):
        return Set.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, item):
        return item.get_absolute_url()


class MacaronCollectionSitemap(Sitemap):
    changefreq = 'always'
    priority = 0.8

    def items(self):
        return Collection.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, item):
        return item.get_absolute_url()
