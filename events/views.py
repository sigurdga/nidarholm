from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from events.models import Event
from events.forms import EventForm
from django.template.context import RequestContext
from django.views.generic import list_detail, date_based
from datetime import date

DATEFIELD = 'start'
MONTH_FORMAT = '%m'

def upcoming_events(request, page=1):

    return list_detail.object_list(request,
                                   queryset=Event.objects.for_user(request.user).filter(start__gt=date.today()),
                                   page=page,
                                   )

def event_archive_year(request, year):
    return date_based.archive_year(request, year, Event.objects.for_user(request.user), DATEFIELD,
                                   make_object_list=True,
                                   allow_future=True,
                                   )

def event_archive_month(request, year, month):
    return date_based.archive_month(request, year, month, Event.objects.for_user(request.user), DATEFIELD,
                                    month_format=MONTH_FORMAT,
                                    allow_future=True,
                                    )

def event_archive_day(request, year, month, day):
    return date_based.archive_day(request, year, month, day, Event.objects.for_user(request.user), DATEFIELD,
                                  month_format=MONTH_FORMAT,
                                  allow_future=True,
                                  )

def event_object_detail(request, year, month, day, slug):
    return date_based.object_detail(request, year, month, day, Event.objects.for_user(request.user), DATEFIELD,
                                    month_format=MONTH_FORMAT,
                                    slug=slug,
                                    allow_future=True,
                                    )

def edit_event(request, id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=id)
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save(commit=False)
            event.user = request.user
            event.save()
            return HttpResponseRedirect(event.get_absolute_url())
    else:
        event = get_object_or_404(Event, id=id)
        form = EventForm(instance=event)
    return render_to_response('events/new_event.html', {'form': form}, context_instance=RequestContext(request))

def new_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return HttpResponseRedirect('/events')
    else:
        event = Event()
        form = EventForm(instance=event)
    return render_to_response('events/new_event.html', {'form': form}, context_instance=RequestContext(request))
