from datetime import timedelta
from math import trunc
from django import template
from django.template.defaultfilters import floatformat
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter
def ellapsed_time(value: timedelta):
    hours: int = value.total_seconds() // 3600
    minutes: int = (value.total_seconds() % 3600) // 60

    def format_number(number) -> str:
        number = int(number)
        if number < 10:
            return f"0{number}"
        else:
            return f"{number}"

    return f"{format_number(hours)}:{format_number(minutes)}"


@register.filter
def currency(value):
    value = intcomma(floatformat(value, 2), True)
    return f"R$ {value}"