# coding: utf-8

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from events.models import Event
from events.forms import EventForm
from django.template.context import RequestContext
from django.views.generic import date_based, DayArchiveView, MonthArchiveView, ArchiveIndexView, DeleteView
from django.views.generic.list import BaseListView
import calendar
from collections import OrderedDict
from datetime import date, datetime, time, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Q
import vobject
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
        month_end = month_start + relativedelta(days=+40) # plus some (makes sure we get the extra days for next month marked)
        future_qs = self.get_queryset().filter(start__gte=today, start__lt=today+relativedelta(months=+3)).order_by("start")
        month_qs = self.get_queryset().filter(start__gt=month_start, start__lt=month_end).order_by("start")
        dates_with_events = set()
        for event in month_qs.all():
            start = event.start.date()
            dates_with_events.add(start)
            if event.end:
                end = event.end.date()
                while start < end:
                    start += relativedelta(days=+1)
                    dates_with_events.add(start)
        week_list = make_calendar_context(today.year, today.month, dates_with_events)

        context['calendar'] = week_list
        context['upcoming'] = future_qs
        context['month'] = today
        context['previous_month'] = today + relativedelta(months=-1)
        context['next_month'] = today + relativedelta(months=+1)
        return context

class EventVobjectView(BaseListView):
    model = Event

    def get_queryset(self):
        one_year_ago = date.today() - timedelta(365)
        qs = super(EventVobjectView, self).get_queryset().filter(start__gte=one_year_ago, group__isnull=True)
        return qs

    def render_to_response(self, context):
        cal = vobject.iCalendar()
        cal.add('method').value = 'PUBLISH'
        cal.add('calscale').value = 'GREGORIAN'
        cal.add('x-original').value = "http://" + self.request.get_host() + reverse('events-archive')
        for event in self.get_queryset():
            e = cal.add('vevent')
            e.add('url').value = "http://" + self.request.get_host() + event.get_absolute_url()
            e.add('summary').value = event.title
            e.add('description').value = event.content
            if event.location:
                e.add('location').value = event.location
            e.add('dtstamp').value = datetime.now()
            if event.whole_day or event.start.time() == time(0,0,0):
                e.add('dtstart').value = event.start.date()
                if not event.end or event.end == event.start:
                    e.add('dtend').value = event.start.date() + timedelta(1)
                else:
                    e.add('dtend').value = event.end.date()

            else:
                e.add('dtstart').value = event.start
                if event.end:
                    e.add('dtend').value = event.end
                else:
                    e.add('dtend').value = event.start

        icalstream = cal.serialize()
        response = HttpResponse(icalstream, mimetype='text/calendar')
        name = slugify(self.request.organization.site.name)
        response['Filename'] = name + '.ics'  # IE needs this
        response['Content-Disposition'] = 'attachment; filename=' + name + '.ics'
        return response


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
        dates_with_events = set()
        for event in self.get_queryset():
            start = event.start.date()
            dates_with_events.add(start)
            if event.end:
                end = event.end.date()
                while start < end:
                    start += relativedelta(days=+1)
                    dates_with_events.add(start)
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
        month_end = month_start + relativedelta(months=+1)
        day = date(year=year, month=month, day=int(self.kwargs['day']))
        month_qs = self.get_queryset().filter(start__gte=month_start, start__lt=month_end).order_by("start")
        day_qs = self.get_queryset().filter(Q(end__isnull=True, start__range=(day, day))|Q(end__gte=day,start__lte=day))
        dates_with_events = set()
        for event in month_qs.all():
            start = event.start.date()
            dates_with_events.add(start)
            if event.end:
                end = event.end.date()
                while start < end:
                    start += relativedelta(days=+1)
                    dates_with_events.add(start)

        week_list = make_calendar_context(year, month, dates_with_events)
        context['calendar'] = week_list
        context['present'] = day_qs
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
    return render_to_response('events/new_event.html', {'form': form, 'object': event}, context_instance=RequestContext(request))

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

class EventDeleteView(DeleteView):

    model = Event

    def get_success_url(self):
        return reverse('events-archive')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(EventDeleteView, self).dispatch(*args, **kwargs)
