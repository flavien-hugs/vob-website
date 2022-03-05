# checkout.models.py

from django.contrib import admin
from django.utils.html import format_html
from checkout.models import Checkout, RegisterCourse
from checkout.ressources import(
    CheckoutBookResource, RegisterCourseBookResource
)

from import_export.formats import base_formats
from import_export.admin import ExportActionMixin


@admin.register(Checkout)
class CheckoutAdmin(ExportActionMixin, admin.ModelAdmin):
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
                    'payment',
                    ('transaction_number', 'transaction_code'),
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
        'get_payment_type',
        'book', 'get_book_cost',
        'get_delivery', 'get_order_book',
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
    formats = [base_formats.XLSX]
    resource_class = CheckoutBookResource


@admin.register(RegisterCourse)
class RegisterCourseAdmin(ExportActionMixin, admin.ModelAdmin):
    model = RegisterCourse
    list_per_page = 10
    date_hierarchy = 'created_at'
    fieldsets = (
        ('commandes',
            {
                'fields': (
                    'course',
                    ('first_name', 'last_name'),
                    'email',
                    ('phone', 'phone_two'),
                    ('city', 'country'),
                    'ip_address',
                )
            }
         ),
    )
    list_display = [
        'id_checkout', 'full_name',
        'course', 'get_course_cost',
        'city', 'get_signup_course',
    ]
    list_filter = ['course', 'created_at']
    search_fields = [
        'id_checkout',
        'phone',
    ]
    readonly_fields = [
        'course',
        'first_name', 'last_name', 'email',
        'phone', 'phone_two',
        'city', 'country', 'ip_address',
    ]
    list_display_links = ['id_checkout', 'full_name']
    formats = [base_formats.CSV]
    resource_class = RegisterCourseBookResource
