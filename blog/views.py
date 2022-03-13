# blog.views.py

import json
import random

from django.http import Http404
from django.urls import reverse
from django.views import generic

from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect, get_object_or_404


from blog.forms import CommentForm
from blog.models import Post, Category, Comment


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
        kwargs['object'] = self.category
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


class PostDetailView(generic.DetailView, generic.edit.FormView):
    model = Post
    slug_field = "slug"
    slug_url_kwarg = "slug"
    form_class = CommentForm
    template_name = "blog/_detail.html"

    def get_object(self):
        try:
            my_object = Post.objects.get(
                slug=self.kwargs.get('slug')
            )
            return my_object
        except self.model.DoesNotExist:
            raise Http404("No MyModel matches the given query.")

    def get_success_url(self):
        return reverse(self.get_object().get_absolute_url())

    def get_context_data(self, **kwargs):
        
        comments = self.object.comment_list()

        kwargs['form'] = self.form_class()
        kwargs['comments'] = comments
        kwargs['comments_count'] = len(comments) if comments else 0

        post = self.get_object()
        kwargs['page_title'] = f"{post.name}"

        # List of similar posts
        similar_post_filter = sorted(self.model.objects.related(
            instance=post)[:10], key=lambda x: random.random()
        )

        kwargs['next_post'] = self.object.next_post
        kwargs['prev_post'] = self.object.prev_post
        kwargs['post_similary'] = similar_post_filter

        return super().get_context_data(**kwargs)

    def post(self, form):
        
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return super(PostDetailView, self).form_valid(form)


post_detail_view = PostDetailView.as_view()


class CommentPostView(generic.edit.FormView):
    form_class = CommentForm
    template_name = "blog/_detail.html"

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super(CommentPostView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        post = Post.objects.get(slug=self.kwargs['slug'])
        return redirect(post.get_absolute_url())

    def get_success_url(self):
        post = Post.objects.get(slug=self.kwargs['slug'])
        return reverse_lazy(post.get_absolute_url())

    def form_invalid(self, form):
        
        post = Post.objects.get(slug=self.kwargs['slug'])
        return self.render_to_response({
            'form': form,
            'post': post
        })

    def form_valid(self, form):
        post_slug = self.kwargs['slug']
        post = Post.objects.get(slug=post_slug)

        comment = form.save(False)
        comment.post = post

        if form.cleaned_data['parent_comment_id']:
            parent_comment = Comment.objects.get(
                pk=form.cleaned_data['parent_comment_id']
            )
            comment.parent_comment = parent_comment

        comment.save(True)

        return redirect(post.get_absolute_url())


comment_post_view = CommentPostView.as_view()
