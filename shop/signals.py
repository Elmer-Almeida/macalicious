from django.db.models.signals import pre_save, post_save

from macalicious.utils import unique_slug_generator, random_string_generator_alternate

from .models import Tag, Macaron, Image, Set, \
    Collection, CollectionImage, CustomCollection, CustomCollectionType


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        prefix = "tag_"
        instance.slug = unique_slug_generator(instance, prefix, instance.name)


pre_save.connect(tag_pre_save_receiver, sender=Tag)


def macaron_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        prefix = "macaron_"
        instance.slug = unique_slug_generator(instance, prefix, instance.name)


pre_save.connect(macaron_pre_save_receiver, sender=Macaron)


def macaron_set_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        prefix = "box_"
        instance.slug = unique_slug_generator(instance, prefix, instance.macaron.name)


pre_save.connect(macaron_set_pre_save_receiver, sender=Set)


def macaron_collection_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        prefix = "collection_"
        instance.slug = unique_slug_generator(instance, prefix, instance.name)


pre_save.connect(macaron_collection_pre_save_receiver, sender=Collection)


def macaron_image_post_save_receiver(sender, instance, *args, **kwargs):
    featured_exists = False
    # Check if there are any featured images that belong to the macaron
    for image in instance.macaron.images.all():
        if image.featured:
            featured_exists = True
    # Make the first image the featured if nothing is selected
    if not featured_exists:
        first = instance.macaron.images.first()
        first.featured = True
        first.save()


post_save.connect(macaron_image_post_save_receiver, sender=Image)


def macaron_collection_image_post_save_receiver(sender, instance, *args, **kwargs):
    featured_exists = False
    for image in instance.collection.images.all():
        if image.featured:
            featured_exists = True
    if not featured_exists:
        first = instance.collection.images.first()
        first.featured = True
        first.save()


post_save.connect(macaron_collection_image_post_save_receiver, sender=CollectionImage)


def macaron_custom_collection_type_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance, 'type_', instance.name)


pre_save.connect(macaron_custom_collection_type_pre_save_receiver, sender=CustomCollectionType)


def macaron_custom_collection_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = random_string_generator_alternate('slug_', 15)


pre_save.connect(macaron_custom_collection_pre_save_receiver, sender=CustomCollection)
