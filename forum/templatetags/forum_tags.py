from django import template
from forum.models import Debate
from django.template.defaultfilters import date, time

from datetime import datetime, timedelta

register = template.Library()

@register.simple_tag
def last_commented(request):
    tops = []
    already_there = set()
    debates = Debate.objects.for_user(request.user).order_by("-created").filter(created__gt=datetime.now()-timedelta(days=366))
    for debate in debates:
        top = debate.get_top()
        if not top in already_there:
            already_there.add(top)
            tops.append((top.title, top.get_absolute_url(), debate.created, debate.user))
    return html_list(tops)

def html_list(list):
    ret = '<ul>'
    for debate in list:
        title, url, created, user = debate
        ret += '<li><a href="%s">%s</a><br />%s, %s' % (url, title, user.get_full_name(), date(created, "DATE_FORMAT") + " " + time(created, "TIME_FORMAT"))
    ret += '</ul>'
    return ret
