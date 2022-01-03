# course.admin.py

from typing import Set
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from course.models import Course, Book
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Course)
class CourseAdmin(SummernoteModelAdmin):
    model = Course
    list_per_page = 10
    date_hierarchy = "published"
    fieldsets = (
        (
            'Information sur la formation', {
                'fields': (
                    "name", "subtitle",
                    "price", "date_of_course",
                    'location_of_course',
                )
            }
        ),
        (
            'Description de la formation', {
                'fields': (
                    "resume",
                    "description",
                    "cover",
                    ("option", "status"),
                    "published"
                )
            }
        ),
    )
    list_display = [
        "name",
        "view",
        "status",
        "option",
        "show_course_url",
        "created_at",
    ]
    list_display_links = [
        'name',
    ]
    list_filter = (
        "status",
        "option",
    )
    list_editable = (
        "option",
        "status",
    )
    search_fields = (
        "name",
        "status",
        "option",
    )
    
    @mark_safe
    @admin.display(description="Voir la formation")
    def show_course_url(self, instance):
        url = instance.get_absolute_url()
        response = format_html(f"""<a target="_blank" href="{url}">{url}</a>""")
        return response
    
    def has_delete_permission(self, request, obj=None):
        return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = Set()
        
        if is_superuser:
            disabled_fields |= {
                'email',
                'username',
                'is_active',
                'is_staff',
                'is_superuser',
                'user_permissions',
            }

        if (
            not is_superuser
            and obj is not None
            and obj == request.user
        ):
            disabled_fields |= {
                'groups',
                'is_staff',
                'is_superuser',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True
        return form


@admin.register(Book)
class BookAdmin(SummernoteModelAdmin):
    model = Book
    list_per_page = 10
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "Descrire l'article", {
                'fields': (
                    "name",
                    "price",
                    "resume",
                    "cover",
                    "status",
                )
            }
        ),
    )
    list_display = [
        "name",
        "price",
        "status",
        "view",
        "show_item_url",
        "created_at",
    ]
    list_display_links = [
        'name',
    ]
    list_filter = (
        "status",
    )
    list_editable = (
        "status",
    )
    search_fields = (
        "name",
        "status",
    )
    
    @mark_safe
    @admin.display(description="Voir l'article")
    def show_item_url(self, instance):
        url = instance.get_absolute_url()
        response = format_html(f"""<a target="_blank" href="{url}">{url}</a>""")
        return response
