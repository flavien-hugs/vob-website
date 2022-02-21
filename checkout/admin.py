# checkout.models.py

from django.contrib import admin
from django.utils.html import format_html
from checkout.models import Checkout


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    model = Checkout
    list_per_page = 10
    date_hierarchy = 'created_at'
    fieldsets = (
        ('commandes',
            {
                'fields': (
                    'book',
                    ('first_name', 'last_name'),
                    'email',
                    ('phone', 'phone_two'),
                    'address',
                    ('city', 'country'),
                    'ip_address',
                )
            }
         ),
    )
    list_display = [
        'id_checkout', 'full_name',
        'book', 'get_book_cost',
        'get_delivery', 'date',
    ]
    list_filter = ['created_at']
    search_fields = [
        'id_checkout',
        'phone',
    ]
    readonly_fields = [
        'book',
        'first_name', 'last_name', 'email',
        'phone', 'phone_two', 'address',
        'city', 'country', 'ip_address',
    ]
    list_display_links = ['id_checkout', 'full_name']
