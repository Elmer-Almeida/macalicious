import json
import random
import string
import urllib

from django.conf import settings
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


# handle recpatcha response
def handle_recaptcha_response(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    recaptcha_response_url = 'https://www.google.com/recaptcha/api/siteverify'
    recaptcha_response_values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    recaptcha_data = urllib.parse.urlencode(recaptcha_response_values).encode()
    recaptcha_request = urllib.request.Request(recaptcha_response_url, data=recaptcha_data)
    recaptcha_response = urllib.request.urlopen(recaptcha_request)
    recaptcha_result = json.loads(recaptcha_response.read().decode())
    return recaptcha_result
