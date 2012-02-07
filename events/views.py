from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from events.models import Event
from events.forms import EventForm
from django.template.context import RequestContext
from django.views.generic import date_based, DayArchiveView, MonthArchiveView, ArchiveIndexView
from datetime import date
import calendar
from collections import OrderedDict
from datetime import date
from dateutil.relativedelta import relativedelta

DATEFIELD = 'start'
MONTH_FORMAT = '%m'

def make_calendar_context(year, month, activity_date_list):
    cal = calendar.Calendar()
    week_list = OrderedDict()
    today = date.today()
    for day in cal.itermonthdates(year, month):
        week_number = int(day.strftime("%W"))
        if week_number == 0:
            week_number = week_list.keys()[-1]
        if not week_number in week_list:
            week_list[week_number] = []
        week_list[week_number].append((
            int(day.strftime("%d")),
            day in activity_date_list,
            day.month==month,
            day==today,
            ))
    return week_list

class EventArchiveIndexView(ArchiveIndexView):
    model = Event
    date_field = DATEFIELD
    allow_future = True

    def get_context_data(self, **kwargs):
        context = super(EventArchiveIndexView, self).get_context_data(**kwargs)
        today = date.today()
        month_start = today.replace(day=1)
        month_end = today.replace(month=today.month+1) # plus some
        future_qs = self.get_queryset().filter(start__gte=today, start__lt=today+relativedelta(months=+3)).order_by("start")
        month_qs = self.get_queryset().filter(start__gt=month_start, start__lt=month_end).order_by("start")
        dates_with_events = [ d.date() for d in self.get_date_list(month_qs, 'day') ]
        week_list = make_calendar_context(today.year, today.month, dates_with_events)

        context['calendar'] = week_list
        context['upcoming'] = future_qs
        context['month'] = today
        context['previous_month'] = today + relativedelta(months=-1)
        context['next_month'] = today + relativedelta(months=+1)
        return context


def event_archive_year(request, year):
    return date_based.archive_year(request, year, Event.objects.for_user(request.user), DATEFIELD,
                                   make_object_list=True,
                                   allow_future=True,
                                   )


class EventMonthArchiveView(MonthArchiveView):
    model = Event
    date_field = DATEFIELD
    allow_future = True
    allow_empty = True
    month_format = MONTH_FORMAT

    def get_context_data(self, **kwargs):
        context = super(EventMonthArchiveView, self).get_context_data(**kwargs)
        dates_with_events = [ datetime.date() for datetime in kwargs['date_list'] ]
        month = int(self.kwargs['month'])
        year = int(self.kwargs['year'])
        week_list = make_calendar_context(year, month, dates_with_events)
        context['calendar'] = week_list
        return context

class EventDayArchiveView(DayArchiveView):
    model = Event
    date_field = DATEFIELD
    allow_future = True
    allow_empty = True
    month_format = MONTH_FORMAT

    def get_context_data(self, **kwargs):
        context = super(EventDayArchiveView, self).get_context_data(**kwargs)
        month = int(self.kwargs['month'])
        year = int(self.kwargs['year'])
        month_start = date(year=year, month=month, day=1)
        month_end = date(year=year, month=month+1, day=1)
        month_qs = self.get_queryset().filter(start__gt=month_start, start__lt=month_end).order_by("start")
        dates_with_events = [ d.date() for d in self.get_date_list(month_qs, 'day') ]
        week_list = make_calendar_context(year, month, dates_with_events)
        context['calendar'] = week_list
        context['month'] = month_start
        context['previous_month'] = month_start + relativedelta(months=-1)
        context['next_month'] = month_start + relativedelta(months=+1)
        return context

def event_archive_day(request, year, month, day):
    return date_based.archive_day(request, year, month, day, Event.objects.for_user(request.user), DATEFIELD,
                                  month_format=MONTH_FORMAT,
                                  allow_future=True,
                                  allow_empty=True,
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
