# course.admin.py

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
                    "option",
                    "published",
                )
            }
        ),
    )
    list_display = [
        "name",
        "course_price",
        "course_count_viewed",
        "option",
        "show_course_url",
        "published",
    ]
    list_display_links = [
        'name',
    ]
    list_filter = (
        "option",
    )
    list_editable = (
        "option",
    )
    search_fields = (
        "name",
        "option",
    )
    
    @mark_safe
    @admin.display(description="Voir la formation")
    def show_course_url(self, instance):
        url = instance.get_absolute_url()
        response = format_html(f"""<a target="_blank" href="{url}">{url}</a>""")
        return response


@admin.register(Book)
class BookAdmin(SummernoteModelAdmin):
    model = Book
    list_per_page = 10
    date_hierarchy = "created_at"
    fieldsets = (
        (
            "Descrire l'article", {
                'fields': (
                    ("name", "price"),
                    "resume",
                    "cover",
                    "published",
                )
            }
        ),
    )
    list_display = [
        "name",
        "book_price",
        "book_count_viewed",
        "published", "show_item_url",
    ]
    list_display_links = [
        'name',
    ]
    search_fields = (
        "name",
    )
    
    @mark_safe
    @admin.display(description="Voir l'article")
    def show_item_url(self, instance):
        url = instance.get_absolute_url()
        response = format_html(f"""<a target="_blank" href="{url}">{url}</a>""")
        return response
