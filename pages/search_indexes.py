from haystack import indexes
from haystack import site
from pages.models import FlatPage

class PageIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    user = indexes.CharField(model_attr='user')
    group = indexes.CharField(model_attr='group', null=True)

    def get_model(self):
        return FlatPage

    def index_queryset(self):
        return self.get_model().objects.all()

site.register(FlatPage, PageIndex)
