from django.conf.urls.defaults import patterns
from events.views import *

urlpatterns = patterns('',
    (r'^$', upcoming_events, (), 'events-list'),
    (r'^new$', new_event, (), 'events-new'),
    (r'^(?P<id>\d+)/edit$', edit_event, (), 'events-edit'),
    (r'^archive$', event_archive, (), 'events-archive'),
    (r'^(?P<year>\d{4})$', event_archive_year, (), 'events-year'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})$', event_archive_month, (), 'events-month'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})$', event_archive_day, (), 'events-month'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)$', event_object_detail, (), 'events-event'),
)
