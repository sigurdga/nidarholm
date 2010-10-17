from django.conf.urls.defaults import *
from relations.views import group_category_list, group_category_detail

urlpatterns = patterns('',
    (r'^$', group_category_list, (), 'relations-group-category-list'),
    (r'^(?P<slug>[-\w]+)$', group_category_detail, (), 'relations-group-category-detail'),
)
