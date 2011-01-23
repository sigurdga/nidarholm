from django.conf.urls.defaults import *
from organization.views import group_category_list, group_category_detail

urlpatterns = patterns('',
    (r'^$', group_category_list, (), 'organization-group-category-list'),
    (r'^(?P<slug>[-\w]+)/(?P<group_slug>[-\w]+)/$', group_category_detail, (),
            'organization-group-category-detail'),
    (r'^(?P<slug>[-\w]+)/(?P<group_slug>[-\w]+)/(?P<status_id>\d+)/$', group_category_detail, (),
            'organization-group-category-detail-status'),
)
