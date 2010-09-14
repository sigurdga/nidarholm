from forum.views import debate_list, debate_tree, new_debate
from django.conf.urls.defaults import patterns

urlpatterns = patterns('django.views.generic.list_detail',
        (r'^(?P<slug>[-\w]+)/new$', new_debate, (), 'new_debate'),
        (r'^(?P<slug>[-\w]+)$', debate_tree, (), 'forum_debate'),
        (r'^$', debate_list, (), 'debate_list'),
        )
