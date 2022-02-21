# course.views.py

from django.urls import reverse
from django.views import generic
from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import SingleObjectMixin

from course.models import Book


class BookListView(generic.ListView):
    model = Book
    paginate_by = 6
    template_name = "book/_list.html"

    def get_queryset(self):
        return Book.objects.published()

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = "Livre en vente"
        return super().get_context_data(**kwargs)


book_list_view = BookListView.as_view()


class BookDetailView(SingleObjectMixin, generic.ListView):
    paginate_by = 2
    template_name = "book/_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=Book.objects.published()
        )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = f"{self.object.name}"
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return Book.objects.published()


book_detail_view = BookDetailView.as_view()
