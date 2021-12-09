from django.db import models


class CartManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset().filter(active=True)


class CartItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all(self):
        return self.get_queryset().filter(active=True)

    def active(self):
        return self.get_queryset().filter(active=True)

    def inactive(self):
        return self.get_queryset().filter(active=False)
