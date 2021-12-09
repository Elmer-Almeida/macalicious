from django.db import models


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


class MacaronImageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset().filter(active=True)

    def featured(self):
        return self.all().filter(featured=True).first()

    def gallery(self):
        return self.all().filter(featured=False)


class MacaronSetManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset().filter(active=True)

    def featured(self):
        return self.all().filter(featured=True)

    # get 3 items of the featured to display as recommendations - CART
    def recommended(self):
        return self.featured()[:3]


class MacaronCollectionItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset().filter(active=True)


class MacaronCollectionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset().filter(active=True)

    def featured(self):
        return self.all().filter(featured=True)

    # get 3 of the featured to display as recommended
    def recommended(self):
        return self.featured()[:3]


class MacaronCollectionImageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset().filter(active=True)

    def featured(self):
        return self.all().filter(featured=True).first()

    def gallery(self):
        return self.all().filter(featured=False)
