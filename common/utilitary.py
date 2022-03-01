# common.utilitary.py

import os
import logging
from hashlib import sha256

from django.utils.text import slugify
from django.utils.crypto import get_random_string

logger = logging.getLogger(__name__)


def upload_image_to(instance, filename):
    ext = filename.split(".")[-1]
    if instance.name:
        filename = f"{instance.name}.{ext}".lower()
    return os.path.join(instance.file_prepend, filename)


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name.replace(' ', '-'))

    Klass = instance.__class__

    while Klass.objects.filter(slug=slug).exists():
        new_slug = f"{slug}-{get_random_string(6)}".lower()
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', None)
    return ip


def cache_decorator(expiration=3 * 60):
    def wrapper(func):
        def news(*args, **kwargs):
            try:
                view = args[0]
                key = view.get_cache_key()
            except BaseException:
                key = None
            if not key:
                unique_str = repr((func, args, kwargs))

                m = sha256(unique_str.encode('utf-8'))
                key = m.hexdigest()
            value = cache.get(key)
            if value is not None:
                if str(value) == '__default_cache_value__':
                    return None
                else:
                    return value
            else:
                logger.info(f"cache_decorator set cache:{func.__name__} key:{key}")
                value = func(*args, **kwargs)
                if value is None:
                    cache.set(key, '__default_cache_value__', expiration)
                else:
                    cache.set(key, value, expiration)
                return value
        return news

    return wrapper
