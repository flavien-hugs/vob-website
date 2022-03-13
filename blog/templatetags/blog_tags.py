# blog.templatetags.blog_tags.py

import random

from django import template
from django.db.models import Count

from blog.models import Category, Post

register = template.Library()


@register.inclusion_tag("blog/paths/__post_category.html")
def post_category_list(count=6):
    categories = Category.objects.all()[:count]
    category_random = sorted(categories, key=lambda x: random.random())
    return {'category_object_list': category_random}


@register.inclusion_tag("blog/paths/__post_news.html")
def post_news_list(count=3):
    posts = Post.objects.published()[:count]
    post_random = sorted(posts, key=lambda x: random.random())
    return {'article_object_list': post_random}


@register.simple_tag
def get_most_commented_posts(count=5):

    most_commented_posts = Post.objects.published().annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

    return most_commented_posts
