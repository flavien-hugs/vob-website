# blog.templatetags.blog_tags.py

import random

from django import template

from course.models import Course

register = template.Library()


@register.inclusion_tag("course/paths/__course_news.html")
def course_news_list(count=3):
    courses = Course.objects.published()[:count]
    course_random = sorted(courses, key=lambda x: random.random())
    return {'course_object_list': course_random}
