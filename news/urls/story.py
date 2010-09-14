from forum.views import story_list, story, new_story
from django.conf.urls.defaults import patterns

urlpatterns = patterns('django.views.generic.list_detail',
        (r'^(?P<slug>[-\w]+)/new$', new_story, (), 'new_story'),
        (r'^(?P<slug>[-\w]+)$', story, (), 'story'),
        (r'^$', story_list, (), 'news_list'),
        )
