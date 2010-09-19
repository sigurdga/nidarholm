from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from events.models import Event
from events.forms import EventForm

def event_list(request, event_category=None):
    event_list = Event.objects.filter(event_category=event_category)
    paginator = Paginator(event_list, 25)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        event_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        event_page = paginator.page(paginator.num_pages)

    return render_to_response('events/list.html', {'events': event_page})

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
            return HttpResponseRedirect('/events')
    else:
        event = get_object_or_404(Event, id=id)
        form = EventForm(instance=event)
    return render_to_response('events/new_event.html', {'form': form})

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
    return render_to_response('events/new_event.html', {'form': form})
