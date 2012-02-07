# coding: utf-8
from django import template
from events.models import Event

from datetime import datetime
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

register = template.Library()

@register.simple_tag
def next_of_category(category_name, user):
    events = Event.objects.for_user(user).filter(event_category__title=category_name).filter(start__gte=datetime.now()).order_by('-start')[:1]
    if events:
        event = events[0]
        return "<div class=\"next\"><p><a href=\"" + event.get_absolute_url() + "\">" + event.title + "</a><p>" + event.start.strftime("%Y-%m-%d %H:%M") + "</p></div>"

@register.simple_tag(takes_context=True)
def format_calendar(context):
    month = context['month']
    retval = '<table class="month">'
    retval += '<thead><tr><th class="wno">%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>' % (_('week'), _('mo'), _('tu'), _('we'), _('th'), _('fr'), _('sa'), _('su'))
    for weeknum, week in context['calendar'].items():
        retval += "<tr>"
        retval += '<th class="wno">%d</th>' % weeknum
        for day in week:
            dno, activities, this_month, today = day
            classes = []
            if activities:
                classes.append("activities")
            if not this_month:
                classes.append("other_month")
            if today:
                classes.append("today")

            class_string = " ".join(classes)
            if class_string:
                class_string = ' class="%s"' % class_string
            url = reverse('events-day', args=[month.year, month.month, dno])
            retval += '<td%s><a style="display:block" href="%s">%d</a></td>' % (class_string, url, dno)
        retval += "</tr>"
    retval += "</tbody></table>"
    return retval
