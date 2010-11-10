from django.conf.urls.defaults import *
from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView
from search.views import RestrictedSearchView
from search.forms import RestrictedSearchForm

urlpatterns = patterns('haystack.views',
    url(r'^$', SearchView(
        template='search/search.html',
        form_class=ModelSearchForm,
    ), name='haystack_search'),
)
