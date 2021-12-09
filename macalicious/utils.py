import time
import random
import string

from django.utils.text import slugify


# Generate string of random characters
def random_string_generator(prefix, size=12, chars=string.digits + string.ascii_uppercase):
    return prefix + ''.join(random.choice(chars) for _ in range(size))


# Generate unique slugs
def unique_slug_generator(instance, prefix, name, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(prefix, size=10)
        )
        return unique_slug_generator(instance, prefix, name, new_slug=new_slug)
    return slug
