# blog.views.py

from django.urls import reverse
from django.views import generic

from blog.models import Post, Category


class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 6
    context_object_name = 'posts_list'
    template_name = "blog/post_list.html"

    def get_queryset(self):
        category = self.model.objects.get(slug=self.kwargs['slug'])
        post_in_category = Post.objects.filter(category=category).published()
        return post_in_category

    def get_context_data(self, **kwargs):
        category = self.model.objects.get(slug=self.kwargs['slug'])
        kwargs['page_title'] = f"{category.name}".capitalize()
        return super().get_context_data(**kwargs)


category_list = CategoryListView.as_view()


class PostListView(generic.ListView):
    paginate_by = 6
    context_object_name = "posts"
    queryset = Post.objects.published()
    template_name = "blog/post_list.html"


post_list_view = PostListView.as_view(
    extra_context={"page_title": "blog"}
)


class PostFreeListView(generic.ListView):
    paginate_by = 6
    queryset = Post.objects.free()
    context_object_name = "posts"
    template_name = "blog/post_list.html"


post_free_list_view = PostFreeListView.as_view(
    extra_context={"page_title": "articles gratuits"}
)


class PostPaidListView(generic.ListView):
    paginate_by = 6
    queryset = Post.objects.paid()
    context_object_name = "posts"
    template_name = "blog/post_list.html"


post_paid_list_view = PostPaidListView.as_view(
    extra_context={"page_title": "articles payants"}
)


class PostDetailView(generic.DetailView):
    model = Post
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "post"
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        post = self.get_object()
        kwargs['page_title'] = f"{post.title}"

        # List of similar articles
        similar_post = self.model.objects.published()
        similar_post_filter = similar_post.exclude(id=post.id).prefetch_related('category')

        return super().get_context_data(**kwargs)


post_detail_view = PostDetailView.as_view()
