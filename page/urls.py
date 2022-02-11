# page.urls.py

from django.urls import path
from django.contrib.flatpages import views

from page.views import contact_view


app_name = 'page'
urlpatterns = [
    path(route='contact/', view=contact_view, name='contact'),
    path('qui-suis-je/', views.flatpage, {'url': '/about-us/'}, name='about_page'),
    path('questions-frequements-posees/', views.flatpage, {'url': '/faq/'}, name='faq_page'),
    path('politique-de-confidentialite/', views.flatpage, {'url': '/terms/'}, name='terms_page'),
    path('conditions-utilisations-generales/', views.flatpage, {'url': '/cgu/'}, name='cgu_page'),
]
