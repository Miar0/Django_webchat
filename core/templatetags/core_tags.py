from datetime import datetime

from django import template
from django.utils import timezone

register = template.Library()


@register.filter(name='convert_to_24H')
def convert_24h(date: datetime) -> str:
    time_obj = timezone.localtime(date)
    return time_obj.strftime('%H:%M')
