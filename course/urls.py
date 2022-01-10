# course.urls.py

from django.urls import path, include

from course.views import course, book


urlpatterns = [
    # courses urls
    path("article/", include(([
        path(route='', view=course.course_list_view, name='course_list'),
        path(route='detail/<slug>/', view=course.course_detail_view, name='course_detail'),
    ], 'course'), namespace='course')),
    
    # books urls
    path("livre/", include(([
        path(route='', view=book.book_list_view, name='book_list'),
        path(route='detail/<slug>/', view=book.book_detail_view, name='book_detail'),
    ], 'course'), namespace='book')),
]
