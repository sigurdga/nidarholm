# -*- encoding: utf-8 -*-

from django import template
from django.template.defaultfilters import date, time

register = template.Library()

@register.simple_tag
def single_datetime(from_date, whole_day=False):
    if whole_day:
        return date(from_date, "DATE_FORMAT")
    else:
        return u"%s, %s" % (
                    date(from_date, "DATE_FORMAT"),
                    time(from_date, "TIME_FORMAT"),
                    )

@register.simple_tag
def between_datetimes(from_date, to_date, whole_day=False):
    if not to_date:
        return single_datetime(from_date, whole_day)
    if whole_day:
        if from_date.day == to_date.day:
            return date(from_date, "DATE_FORMAT")
        else:
            return u"%s – %s" % (
                    date(from_date, "DATE_FORMAT"),
                    date(to_date, "DATE_FORMAT"),
                    )
    else:
        if from_date.day == to_date.day:
            return u"%s, %s – %s" % (
                    date(from_date, "DATE_FORMAT"),
                    time(from_date, "TIME_FORMAT"),
                    time(to_date, "TIME_FORMAT"),
                    )
        else:
            return u"%s, %s – %s, %s" % (
                    date(from_date, "DATE_FORMAT"),
                    time(from_date, "TIME_FORMAT"),
                    date(to_date, "DATE_FORMAT"),
                    time(to_date, "TIME_FORMAT"),
                    )
