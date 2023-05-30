from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def uses_moncomptepro():
    return getattr(settings, "USES_MONCOMPTEPRO", "")
