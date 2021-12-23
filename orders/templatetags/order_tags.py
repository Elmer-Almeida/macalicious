from django.utils.html import mark_safe
from django.utils.timesince import timesince
from django import template

register = template.Library()


@register.filter(name="timesince_custom")
def timesince_custom(date):
    if 'days' in timesince(date):
        return get_date(date)
    else:
        time_output = mark_safe(f"{get_date(date)}")
        return time_output


def get_date(date):
    return date.strftime("%d %B %Y at %-I:%M %p")
