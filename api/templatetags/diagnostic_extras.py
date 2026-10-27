from django.template.defaulttags import register

from data.models import Diagnostic


@register.filter
def menu_frequency(key):
    if not key:
        return None
    try:
        return Diagnostic.MenuVegetarienFrequence[key].label
    except Exception:
        return None


@register.filter
def menu_type(key):
    if not key:
        return None
    try:
        return Diagnostic.MenuVegetarienType[key].label
    except Exception:
        return None
