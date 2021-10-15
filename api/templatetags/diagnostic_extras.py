from django.template.defaulttags import register
from data.models import Diagnostic


@register.filter
def menu_frequency(key):
    if not key:
        return None
    try:
        return Diagnostic.MenuFrequency[key].label
    except Exception:
        return None


@register.filter
def menu_type(key):
    if not key:
        return None
    try:
        return Diagnostic.MenuType[key].label
    except Exception:
        return None
