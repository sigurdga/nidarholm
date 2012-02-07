from django.conf.urls.defaults import patterns
from events.views import *

urlpatterns = patterns('',
    (r'^$', EventArchiveIndexView.as_view(), (), 'events-archive'),
    (r'^new$', new_event, (), 'events-new'),
    (r'^(?P<id>\d+)/edit$', edit_event, (), 'events-edit'),
    (r'^(?P<year>\d{4})$', event_archive_year, (), 'events-year'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', EventMonthArchiveView.as_view(), (), 'events-month'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})$', EventDayArchiveView.as_view(), (), 'events-day'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)$', event_object_detail, (), 'events-event'),
)
