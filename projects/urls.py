from django.conf.urls.defaults import patterns

from projects.views import project_list, project_detail, edit_project, new_project

urlpatterns = patterns('',
        (r'^$', project_list, (), 'project_list'),
        (r'^new/$', new_project, (), 'new_project'),
        (r'^(?P<slug>[-\w]+)/edit/$', edit_project, (), 'edit_project'),
        (r'^(?P<slug>[-\w]+)/$', project_detail, (), 'project_detail'),
        )
