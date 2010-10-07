from events.views import new_event, edit_event
from django.conf.urls.defaults import patterns
from django.views.generic.list_detail import object_list
from django.views.generic.date_based import archive_year, archive_month, archive_day, object_detail

from datetime import date

from events.models import Event
from django.template.context import RequestContext
from django.core.context_processors import request

upcoming_dict = {
                 'queryset': Event.objects.filter(start__gt=date.today()),
                 }

events_year_dict = {
                   'queryset': Event.objects.all(),
                   'date_field': 'start',
                   'make_object_list': True,
                   'allow_future': True,
                   }

events_month_dict = {
                   'queryset': Event.objects.all(),
                   'date_field': 'start',
                   'month_format': '%m',
                   'allow_future': True,
                   }

events_day_dict = {
                   'queryset': Event.objects.all(),
                   'date_field': 'start',
                   'month_format': '%m',
                   'day_format': '%d',
                   'allow_future': True,
                   }

event_dict = {
              'queryset': Event.objects.all(),
              'month_format': '%m',
              'day_format': '%d',
              'date_field': 'start',
              'allow_future': True,
              }

urlpatterns = patterns('django.views.generic.list_detail',
    (r'^$', object_list, upcoming_dict, 'events-list'),
    (r'^new$', new_event, (), 'events-new'),
    (r'^(?P<id>\d+)/edit$', edit_event, (), 'events-edit'),
    (r'^(?P<year>\d{4})$', archive_year, events_year_dict, 'events-year'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})$', archive_month, events_month_dict, 'events-month'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})$', archive_day, events_day_dict, 'events-month'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)$', object_detail, event_dict, 'events-event'),
)
