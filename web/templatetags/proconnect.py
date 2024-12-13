from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def uses_proconnect():
    return getattr(settings, "USES_PROCONNECT", "")
