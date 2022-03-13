# page.templatetags.page_tags.py

import random

from django import template

from page.models import Testimonial, Partner

register = template.Library()


@register.inclusion_tag("paths/__testimonial.html")
def testimonials(count=8):
    testimonial = Testimonial.objects.filter(is_active=True)[:count]
    testimonial_random = sorted(testimonial, key=lambda x: random.random())
    return {'testimonials_list': testimonial_random}


@register.inclusion_tag("paths/__partner.html")
def partners(count=6):
    partner = Partner.objects.filter(is_active=True)[:count]
    partner_random = sorted(partner, key=lambda x: random.random())
    return {'partners_list': partner_random}
