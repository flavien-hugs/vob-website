"""
core URL Configuration
The `urlpatterns` list routes URLs to views.
For more information please see:
https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""

from django.contrib import admin
from django.conf import settings
from django.views import generic
from django.shortcuts import render
from django.urls import path, include

# from django.contrib.sites import Site
from django.conf.urls.static import static
from django.contrib.auth.models import Group

# admin.site.unregister(Site)
# admin.site.unregister(Group)

admin.site.site_header = admin.site.site_title = "Valere Obei"
admin.site.index_title = "Bienvenu sur votre tableau d'administration".capitalize()


from page.views import search_view


def handler404(request, exception, template_name='404.html'):
    context = {
        'page_title': 'Page non trouvée',
    }
    return render(request, template_name, context, status=404)


def handler500(request, template_name='500.html'):
    context = {
        'page_title': 'Quelque chose a mal tourné.',
    }
    return render(request, template_name, context, status=500)


class HomeView(generic.TemplateView):
    template_name = 'index.html'

home_view = HomeView.as_view()


urlpatterns = [
    path(route='', view=home_view, name='home'),
    path(route='search/', view=search_view, name='search'),

    path("", include('course.urls')),
    path("blog/", include('blog.urls')),
    path("", include("checkout.urls")),
    path("ps/", include("page.urls", namespace="page")),

    path('search/', include('haystack.urls')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('jet/', include('jet.urls', 'jet')),
    path('summernote/', include('django_summernote.urls')),
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        route='robots.txt',
        view=generic.TemplateView.as_view(
            template_name='robots.txt',
            content_type='text/plain'
        )
    )
]

handler404 = handler404
handler500 = handler500

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        path('404/', handler404, {'exception': Exception("Page non trouvée !")}),
        path('500/', handler500),
    ]
