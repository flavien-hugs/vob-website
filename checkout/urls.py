# checkout.urls.py

from django.urls import path

from checkout import views


app_name='checkout'
urlpatterns = [
    path(
        route='<slug>/',
        view=views.checkout_book_view,
        name='checkout_path'),

    path(
        route='success/<id_checkout>/',
        view=views.checkout_success_view,
        name='checkout_success_path'),
]
