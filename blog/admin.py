# blog.admin.py

from django.db import models

from django.urls import reverse
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from blog.models import Category, Post, Comment

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
        "date_published",
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


@admin.display(description="Desactiver les commenatires")
def disable_comment_status(modeladmin, request, queryset):
    queryset.update(is_enable=False)

@admin.display(description="Activer les commenatires")
def enable_comment_status(modeladmin, request, queryset):
    queryset.update(is_enable=True)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_per_page = 20
    date_hierarchy = "created_at"
    fieldsets = (
        (
            'Commentaire', {
                'fields': (
                    "post",
                    "parent_comment",
                    "name", "email",
                    "content",
                    "is_enable"
                )
            }
        ),
    )
    list_display = [
        'name',
        'link_to_post',
        'is_enable', 'date'
    ]
    list_display_links = ['name']
    list_filter = ['post', 'is_enable']
    exclude = ['created_at', 'updated_at']
    actions = [disable_comment_status, enable_comment_status]

    @admin.display(description="lien vers l'article")
    def link_to_post(self, obj):
        info = (obj.post._meta.app_label, obj.post._meta.model_name)
        link = reverse('admin:%s_%s_change' % info, args=(obj.post.pk,))
        return format_html(f'<a href="{link}">{obj.post.name}</a>')
