# common.context.py

from django.conf import settings


def context_processor(request):
    return {
        'title': settings.SITE_NAME,
        'addr_email': 'hello@valereobei.com',
        'addr_contact': '(225) 077 772 848',
        'request': request,
    }
