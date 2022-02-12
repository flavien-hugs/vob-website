# blog.templatetags.blog_tags.py

import random

from django import template

from blog.models import Post

register = template.Library()


@register.inclusion_tag("blog/paths/__post_news.html")
def post_news_list(count=3):
    posts = Post.objects.published()[:count]
    post_random = sorted(posts, key=lambda x: random.random())
    return {'article_object_list': post_random}
