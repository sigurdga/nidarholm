from vault.views import new_file, file_list, file_details, send_file
from django.conf.urls.defaults import patterns

urlpatterns = patterns('django.views.generic.list_detail',
        (r'^new$', new_file, (), 'new_file'),
        (r'^get/(?P<id>\d+)$', send_file, (), 'send_file'),
        (r'^(?P<id>\d+)$', file_details, (), 'file_details'),
        (r'^$', file_list, (), 'file_list'),
        )
