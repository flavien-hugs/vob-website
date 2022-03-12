# checkout.urls.py

from django.urls import path, include

from checkout import views


urlpatterns = [
    # checkout book urls
    path("checkout/book/", include(([
        path(
            route='<slug>/process/order/',
            view=views.checkout_book_view,
            name='checkout_path'),
        path(
            route='success/<id_checkout>/',
            view=views.checkout_success_view,
            name='checkout_success_path'),
    ], 'checkout'), namespace='checkout_book')),

    # courses register urls
    path("register/course/", include(([
        path(
            route="<slug>/process/",
            view=views.course_register_view,
            name='register_course_path'),
        path(
            route='success/<id_checkout>/',
            view=views.register_success_view,
            name='register_success_path'),
    ], 'checkout'), namespace='register_course')),
]
