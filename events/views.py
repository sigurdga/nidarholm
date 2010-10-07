from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from events.models import Event
from events.forms import EventForm
from django.template.context import RequestContext

def event_details(request, id):
    event = get_object_or_404(Event, id=id)
    return render_to_response('events/event.html', {'event': event})

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
