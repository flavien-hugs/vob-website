# blog.views.py

import random

from django.urls import reverse
from django.views import generic
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from blog.models import Post, Category


class CategoryListView(
    generic.ListView,
    generic.list.MultipleObjectMixin
):
    model = Post
    paginate_by = 10
    template_name = "blog/_list.html"

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        post_in_category = self.model.objects.filter(category=self.category).published()
        return post_in_category

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = f"{self.category.name}".capitalize()
        return super().get_context_data(**kwargs)


category_list = CategoryListView.as_view()


class PostListView(generic.ListView):
    paginate_by = 10
    queryset = Post.objects.published()
    template_name = "blog/_list.html"


post_list_view = PostListView.as_view(
    extra_context={"page_title": "blog"}
)


class PostFreeListView(generic.ListView):
    paginate_by = 10
    queryset = Post.objects.free()
    template_name = "blog/_list.html"


post_free_list_view = PostFreeListView.as_view(
    extra_context={"page_title": "articles gratuits"}
)


class PostPaidListView(generic.ListView):
    paginate_by = 10
    queryset = Post.objects.paid()
    template_name = "blog/_list.html"


post_paid_list_view = PostPaidListView.as_view(
    extra_context={"page_title": "articles payants"}
)


class PostDetailView(generic.DetailView):
    model = Post
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "blog/_detail.html"

    def get_context_data(self, **kwargs):
        post = self.get_object()
        kwargs['page_title'] = f"{post.name}"

        # List for similary articles
        similar_post_filter = sorted(self.model.objects.related(
            instance=post)[:10], key=lambda x: random.random()
        )

        kwargs['post_similary'] = similar_post_filter
        return super().get_context_data(**kwargs)


post_detail_view = PostDetailView.as_view()


def loading_post_more(request):
    offset = int(request.GET.get('offset'))
    limit = 2
    post_obj = list(Post.objects.published().values()[offset:offset+limit])
    data = {
        'posts': post_obj
    }
    return JsonResponse(data=data)


loading_post = loading_post_more
