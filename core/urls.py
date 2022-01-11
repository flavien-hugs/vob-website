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
from django.conf.urls.static import static

admin.site.site_header = admin.site.site_title = "Valere Obei"
admin.site.index_title = "Bienvenu sur votre tableau d'administration".capitalize()


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

    path('book/', include('course.urls')),
    path('blog/', include('blog.urls', namespace="blog")),
    
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('jet/', include('jet.urls', 'jet')),
    path('summernote/', include('django_summernote.urls')),
    path(settings.ADMIN_URL, admin.site.urls),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = handler404
handler500 = handler500

if settings.DEBUG:
    urlpatterns += [
        path('404/', handler404, {'exception': Exception("Page non trouvée !")}),
        path('500/', handler500),
    ]
