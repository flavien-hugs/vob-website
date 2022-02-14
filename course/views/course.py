# course.views.py

from django.views import generic
from django.shortcuts import get_object_or_404
from django.views.generic.detail import SingleObjectMixin

from course.models import Course


class CourseListView(generic.ListView):
    paginate_by = 6
    queryset = Course.objects.published()
    template_name = "course/_list.html"

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = "Formations"
        return super().get_context_data(**kwargs)


course_list_view = CourseListView.as_view()


class CourseTagListView(generic.ListView, generic.list.MultipleObjectMixin):
    paginate_by = 6
    model = Course
    template_name = "course/_list.html"

    def get_queryset(self):
        self.tags = self.model.tags.tag_model.objects.weight()
        self.tag = get_object_or_404(self.model.tags.tag_model, slug=self.kwargs['tag_slug'])
        course_in_tag = self.model.objects.filter(tags=self.tag)
        return course_in_tag

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = self.tag
        return super().get_context_data(**kwargs)


course_tag_view = CourseTagListView.as_view()


class CourseDetailView(SingleObjectMixin, generic.ListView):
    paginate_by = 2
    template_name = "course/_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=Course.objects.published()
        )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['page_title'] = f"{self.object.name}"
        return super().get_context_data(**kwargs)
    
    def get_queryset(self):
        return Course.objects.published()


course_detail_view = CourseDetailView.as_view()
