# blog.admin.py

from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from blog.models import Category, Post
from django_summernote.admin import SummernoteModelAdmin

admin.site.unregister(Group)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_per_page = 10
    date_hierarchy = "created_at"
    fieldsets = (
        ('Category', {
            'fields': ("name",)
            }
        ),
    )
    list_display = (
        "category_name",
        "post_count",
    )
    list_display_links = [
        'category_name',
    ]
    list_filter = (
        "name",
        "created_at",
    )
    search_fields = (
        "name",
    )


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    model = Post
    list_per_page = 10
    date_hierarchy = "created_at"
    fieldsets = (
        (
            'Article', {
                'fields': (
                    "category",
                    "title",
                    "subtitle",
                    'body',
                    'tags',
                    'cover',
                    ('status', 'reading'),
                )
            }
        ),
    )
    list_display = [
        "category",
        "title",
        "view",
        "reading",
        "status",
        "show_post_url",
        "created_at",
    ]
    list_display_links = [
        'title',
        'category'
    ]
    list_filter = (
        "status",
        "reading",
    )
    list_editable = (
        "reading",
        "status",
    )
    search_fields = (
        "title",
        "status",
        "reading",
    )
    
    @mark_safe
    @admin.display(description="Voir l'article")
    def show_post_url(self, instance):
        url = instance.get_absolute_url()
        response = format_html(f"""<a target="_blank" href="{url}">{url}</a>""")
        return response
