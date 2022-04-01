from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def enable_xp_reservation():
    return getattr(settings, "ENABLE_XP_RESERVATION", "")


@register.simple_tag
def enable_xp_vege():
    return getattr(settings, "ENABLE_XP_VEGE", "")


@register.simple_tag
def enable_partners():
    return getattr(settings, "ENABLE_PARTNERS", "")
