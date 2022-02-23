# page.admin.py

from django.contrib import admin
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin

from page.models import Contact
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


admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
