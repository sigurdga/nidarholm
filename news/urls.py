from news.views import new_story
from django.conf.urls.defaults import patterns
from django.views.generic import date_based

from news.models import Story

story_info_archive = {
              "queryset": Story.objects.filter(parent=None),
              "date_field": "pub_date",
              }
story_info_year = {
                   "queryset": Story.objects.filter(parent=None),
                   "date_field": "pub_date",
                   "make_object_list": True,
                   }

story_info_detail = {
                     "queryset": Story.objects.filter(parent=None),
                     "date_field": "pub_date",
                     "slug_field": "slug",
                     "month_format": "%m",
                     }

urlpatterns = patterns('',
        (r'^(?P<id>\d+)/comment$', new_story, (), 'news-new-story-comment'),
        (r'^new$', new_story, (), 'news-new-story'),
        )

urlpatterns += patterns('',
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', date_based.object_detail, story_info_detail, 'news-story'),
    (r'^(?P<year>\d{4})$', date_based.archive_year, story_info_year, 'news-stories-year'),
    (r'^$', date_based.archive_index, story_info_archive, 'news-stories'),
)
