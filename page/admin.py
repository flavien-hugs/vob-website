# page.admin.py

from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin

from page.models import Contact, Testimonial, Partner
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    model = Contact
    date_hierarchy = 'created_at'
    list_display = [
        'name', 'email',
        'subject', 'date'
    ]
    list_per_page = 10
    search_fields = ['email']
    empty_value_display = '-empty-'
    list_filter = ['created_at', 'subject']
    list_display_links = ('name', 'email')
    readonly_fields = (
        'created_at',
        'name',
        'email',
        'subject',
        'message',
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    model = Testimonial
    date_hierarchy = 'created_at'
    list_display = [
        'name',
        'status',
        'is_active',
        'date'
    ]
    fieldsets = (
        (
            'Témoignage', {
                'fields': (
                    "name", "status",
                    "content", "cover",
                    "is_active",
                )
            }
        ),
    )
    list_per_page = 10
    search_fields = ['full_name']
    empty_value_display = '-empty-'
    list_display_links = ('name',)
    list_filter = ['created_at', 'is_active']


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    model = Partner
    date_hierarchy = 'created_at'
    list_display = [
        'name',
        'is_active',
        'date'
    ]
    fieldsets = (
        (
            'Témoignage', {
                'fields': (
                    "name",
                    "cover",
                    "is_active",
                )
            }
        ),
    )
    list_per_page = 10
    search_fields = ['name']
    empty_value_display = '-empty-'
    list_display_links = ('name',)
    list_filter = ['created_at', 'is_active']


class FlatPageAdmin(SummernoteModelAdmin, FlatPageAdmin):
    fieldsets = (
        ("Editer une page statique", {
            'fields': (
                'title', 'url',
                'content',
                'template_name',
                'sites'
            )
        }),
    )
    list_display_links = ['title']
    list_display = ("title", "url",)
    list_filter = search_fields = []

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
