# course.urls.py

from django.urls import path, include

from course.views import course, book


urlpatterns = [
    # books urls
    path("book/", include(([
        path(route='', view=book.book_list_view, name='book_list'),
        path(route='<slug>/', view=book.book_detail_view, name='book_detail'),
    ], 'course'), namespace='book')),

    # courses urls
    path("course/", include(([
        path(route='', view=course.course_list_view, name='course_list'),
        path(route='<slug>/', view=course.course_detail_view, name='course_detail'),
        path(route='tag/<tag_slug>/', view=course.course_tag_view, name='course_tag_list'),
    ], 'course'), namespace='courses')),
]
