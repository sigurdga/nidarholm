from django.conf.urls.defaults import patterns

from projects.views import project_list, project_detail

urlpatterns = patterns('',
        (r'^$', project_list, (), 'project_list'),
        (r'^(?P<slug>[-\w]+)/$', project_detail, (), 'project_detail'),
        )
