from django import template
from events.models import Event

from datetime import datetime

register = template.Library()

@register.simple_tag
def next_of_category(category_name, user):
    event = Event.objects.for_user(user).filter(event_category__title=category_name).filter(start__gte=datetime.now()).order_by('-start')[0]
    return "<div class=\"next\"><p><a href=\"" + event.get_absolute_url() + "\">" + event.title + "</a><p>" + event.start.strftime("%Y-%m-%d %H:%M") + "</p></div>"
