from forum.views import debate_list, debate_object_detail, new_debate, edit_debate
from django.conf.urls.defaults import patterns

urlpatterns = patterns('django.views.generic.list_detail',
        (r'^$', debate_list, (), 'forum-debate-list'),
        (r'^new/$', new_debate, (), 'forum-new-debate'),
        (r'^(?P<slug>[-\w]+)/comment/$', new_debate, (), 'forum-new-debate-comment'),
        (r'^(?P<slug>[-\w]+)/edit/$', edit_debate, (), 'forum-edit-debate-comment'),
        (r'^(?P<slug>[-\w]+)/$', debate_object_detail, (), 'forum-debate'),
        )
