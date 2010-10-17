from navigation.views import sitemap
from django.conf.urls.defaults import patterns

urlpatterns = patterns('django.views.generic.list_detail',
        (r'^$', sitemap, (), 'sitemap'),
        )
