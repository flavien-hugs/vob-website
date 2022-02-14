# course.urls.py

from django.urls import path, include

from course.views import course, book


urlpatterns = [
    # courses urls
    path("formations/", include(([
        path(route='', view=course.course_list_view, name='course_list'),
        path(route='detail/<slug>/', view=course.course_detail_view, name='course_detail'),
        path(route='tag/<tag_slug>/', view=course.course_tag_view, name='course_tag_list'),
    ], 'course'), namespace='course')),
    
    # books urls
    path("livres/", include(([
        path(route='', view=book.book_list_view, name='book_list'),
        path(route='detail/<slug>/', view=book.book_detail_view, name='book_detail'),
    ], 'course'), namespace='book')),
]
