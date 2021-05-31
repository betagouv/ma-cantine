from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def matomo_id():
    return getattr(settings, "MATOMO_ID", "")
