# common.context.py

from django.conf import settings


def context_processor(request):
    
    SITE_NAME = "Valere Obei"
    
    DESCRIPRION = """
        Passion, Motivation, Business &amp; Entrepreneuriat
    """

    KEYWORDS = """
        Passion, Motivation, Business &amp; Entrepreneuriat
    """

    LOCATION = """
        Air-france 2, Bouaké, Côte d'Ivoire
    """

    ADDR_EMAIL = "hello@valereobei.com"
    ADDR_CONTACT_ONE = "(225) 077 772 848"
    ADDR_CONTACT_TWO = "(225) 077 772 808"

    return {
        'title': SITE_NAME,
        'addr_email': ADDR_EMAIL,
        'site_desc': DESCRIPRION,
        'keywords': KEYWORDS,
        'addr_contact': ADDR_CONTACT_ONE,
        'request': request,
    }
