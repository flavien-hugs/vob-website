# blog.search_indexes.py

import datetime

from haystack import indexes
from blog.models import Category, Post


class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True
    )
    name = indexes.EdgeNgramField(
        model_attr='name'
    )

    def get_model(self):
        return Category
    
    def index_queryset(self, using=None):
        return self.get_model().objects.filter(
            created_at__lte=datetime.datetime.now()
        )


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(
        document=True,
        use_template=True
    )
    name = indexes.EdgeNgramField(
        model_attr='name'
    )
    published = indexes.DateTimeField(
        model_attr='published'
    )

    def get_model(self):
        return Post
    
    def index_queryset(self, using=None):
        return self.get_model().objects.published().filter(
            published__lte=datetime.datetime.now()
        )
