# blog.admin.py

from django.db import models

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from blog.models import Category, Post
from imagekit.admin import AdminThumbnail
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Category)
class CategoryAdmin(SummernoteModelAdmin):
    model = Category
    list_per_page = 10
    date_hierarchy = "created_at"
    fieldsets = (
        ('Category', {
            'fields': ("name", "cover",)
            }
        ),
    )
    list_display = (
        "category_name",
        "post_count",
        "show_cat_url",
        "date",
    )
    list_display_links = [
        'category_name',
    ]
    list_filter = (
        "name",
    )
    search_fields = (
        "name",
    )
    category_cover = AdminThumbnail(image_field='formatted_cover')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            _post_count=models.Count("post", distinct=True)
        )
        return queryset

    @admin.display(description="nombre d'articles")
    def post_count(self, instance):
        return instance._post_count

    @mark_safe
    @admin.display(description="Voir")
    def show_cat_url(self, instance):
        url = instance.get_absolute_url()
        response = format_html(f"""<a target="_blank" href="{url}">Voir</a>""")
        return response


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    model = Post
    list_per_page = 10
    date_hierarchy = "created_at"
    fieldsets = (
        (
            'Article', {
                'fields': (
                    "category", "name",
                    ('reading', "price"),
                )
            }
        ),
        (
            "Description de l'article", {
                'fields': (
                    "subtitle", 'body',
                    'cover', 'published',
                )
            }
        ),
    )
    list_display = [
        "category", "post_name",
        "post_count_viewed",
        "post_price",
        "show_post_url",
        "published",
    ]
    list_display_links = [
        'post_name',
        'category'
    ]
    list_filter = (
        "published",
    )
    search_fields = (
        "name",
        "reading",
    )
    post_cover = AdminThumbnail(image_field='formatted_cover')

    @mark_safe
    @admin.display(description="Voir l'article")
    def show_post_url(self, instance):
        url = instance.get_absolute_url()
        response = format_html(f"""<a target="_blank" href="{url}">Voir l'article</a>""")
        return response
