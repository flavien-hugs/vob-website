# blog.search_indexes.py

from haystack import indexes
from course.models import Course, Book


class CourseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True
    )
    name = indexes.EdgeNgramField(
        model_attr='name'
    )

    def get_model(self):
        return Course
    
    def index_queryset(self, using=None):
        return self.get_model().objects.published()
