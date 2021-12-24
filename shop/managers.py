from django.db import models
from django.db.models import Q


class TagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset().filter(active=True)


class MacaronManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset().filter(active=True)


class ImageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset().filter(active=True)

    def featured(self):
        return self.all().filter(featured=True).first()

    def gallery(self):
        return self.all().filter(featured=False)


class SetManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset().filter(active=True).order_by('order')

    def featured(self):
        return self.all().filter(featured=True)

    # get 3 items of the featured to display as recommendations - CART
    def recommended(self):
        return self.featured()[:3]

    def search(self, query):
        return self.all().filter(
            Q(macaron__name__icontains=query) |
            Q(macaron__description__icontains=query)
        )


class CollectionItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset().filter(active=True)


class CollectionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset().filter(active=True).order_by('order')

    def featured(self):
        return self.all().filter(featured=True)

    # get 3 of the featured to display as recommended
    def recommended(self):
        return self.featured()[:3]

    def search(self, query):
        return self.all().filter(
            Q(macarons__macaron__name__icontains=query) |
            Q(description__icontains=query)
        )


class CollectionImageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset().filter(active=True)

    def featured(self):
        return self.all().filter(featured=True).first()

    def gallery(self):
        return self.all().filter(featured=False)
