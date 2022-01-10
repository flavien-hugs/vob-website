# checkout.models.py

from django.contrib import admin

from checkout.models import Checkout


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    model = Checkout
    raw_id_fields = ['book', 'post']
    list_display = [
        'id_checkout',
        'first_name', 'last_name',
        'email', 'phone', 'book', 'post',
        'city', 'created_at',
    ]
    list_filter = ['created_at']
    search_fields = [
        'id_checkout', 'email',
        'phone', 'phone_two'
    ]
    list_display_links = ['id_checkout', 'first_name']

