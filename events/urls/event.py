from events.views import event_list, event_details, new_event, edit_event
from django.conf.urls.defaults import patterns

urlpatterns = patterns('django.views.generic.list_detail',
        (r'^new$', new_event, (), 'new_event'),
        (r'^(?P<id>\d+)/edit$', edit_event, (), 'edit_event'),
        (r'^(?P<id>\d+)$', event_details, (), 'event_details'),
        (r'^$', event_list, (), 'events_list'),
        )
