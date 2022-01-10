# course.urls.py

from django.urls import path, include

from course import views

app_name = 'course'
urlpatterns = [
    path("article/",
        include([])
    ),
    path("book/",
        include([])
    ),
]
