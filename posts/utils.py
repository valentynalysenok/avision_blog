from time import time

from django.utils.text import slugify


def custom_slugify(slug):
    new_slug = slugify(slug, allow_unicode=True)
    return new_slug + '-' + str(int(time()))
