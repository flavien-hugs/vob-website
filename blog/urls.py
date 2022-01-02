# blog.urls.py

from django.urls import path, include

from blog import views

app_name = 'blog'
urlpatterns = [
    path(route='', view=views.post_list_view, name='post_list'),
    path("article/",
        include([
            path(route='<slug>/', view=views.post_detail_view, name='post_detail'),
            path(route='payant/', view=views.post_paid_list_view, name='post_paid_list'),
            path(route='gratuit/', view=views.post_free_list_view, name='post_free_list'),
        ])
    ),
    path(route='categorie/<slug>/', view=views.category_list, name='category_list'),
]
