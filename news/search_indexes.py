from haystack import indexes
from haystack import site
from news.models import Story

class StoryIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')
    group = indexes.CharField(model_attr='group', null=True)

    def get_model(self):
        return Story

    def index_queryset(self):
        return self.get_model().objects.filter(parent__isnull=True)

site.register(Story, StoryIndex)
