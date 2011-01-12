from django import template
from vault.models import UploadedFile
from news.models import Story
from django.template.defaultfilters import date, time

from datetime import datetime, timedelta

register = template.Library()

@register.simple_tag
def file_list(request, count=10):
    files = UploadedFile.objects.for_user(request.user)[0:count]
    return html_list(files)

def html_list(list):
    ret = "<ul>"
    for file in list:
        ret += "<li><a href=\"" + file.get_absolute_url() + "\">" + file.filename + "</a><br />" + date(file.uploaded, "DATE_FORMAT") + " " + time(file.uploaded, "TIME_FORMAT") + "</li>"
    ret += "</ul>"
    return ret

@register.simple_tag
def last_commented_news(request, count):
    tops = []
    already_seen = set()
    stories = Story.objects.for_user(request.user).order_by("-created").filter(created__gt=datetime.now()-timedelta(days=180))
    counter = 0
    for story in stories:
        if counter >= count:
            break
        top = story.get_top()
        if not top in already_seen:
            counter += 1
            already_seen.add(top)
            tops.append((top.title, top.get_absolute_url(), story.created))
    return format_active_list(tops)

def format_active_list(list):
    ret = '<ul>'
    for debate in list:
        title, url, created = debate
        ret += '<li><a href="%s">%s</a><br />%s' % (url, title, date(created, "DATE_FORMAT") + " " + time(created, "TIME_FORMAT"))
    ret += '</ul>'
    return ret
