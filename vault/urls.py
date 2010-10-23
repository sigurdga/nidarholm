from vault.views import new_file, file_list, file_object_detail, send_file
from django.conf.urls.defaults import patterns

urlpatterns = patterns('django.views.generic.list_detail',
        (r'^new$', new_file, (), 'vault-new-file'),
        (r'^get/(?P<id>\d+)$', send_file, (), 'vault-send-file'),
        (r'^get/(?P<id>\d+)/(?P<size>\d+)$', send_file, (), 'vault-send-file'),
        (r'^(?P<id>\d+)$', file_object_detail, (), 'vault-file'),
        (r'^tags/(?P<tags>.*)$', file_list, (), 'vault-tagged-file-list'),
        (r'^$', file_list, (), 'file_list'),
        )
