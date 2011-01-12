from news.views import new_story, story_year, story_archive, story_detail
from django.conf.urls.defaults import patterns
from django.views.generic import date_based

from news.models import Story

urlpatterns = patterns('',
        (r'^(?P<id>\d+)/comment/$', new_story, (), 'news-new-story-comment'),
        (r'^new/$', new_story, (), 'news-new-story'),
        (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', story_detail, (), 'news-story'),
        (r'^(?P<year>\d{4})$', story_year, (), 'news-stories-year'),
        (r'^$', story_archive, (), 'news-stories'),
        )
