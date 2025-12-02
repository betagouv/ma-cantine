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
def enable_teledeclaration():
    return getattr(settings, "ENABLE_TELEDECLARATION", "")


@register.simple_tag
def enable_dashboard():
    return getattr(settings, "ENABLE_DASHBOARD", "")


@register.simple_tag
def enable_waste_measurements():
    return getattr(settings, "ENABLE_WASTE_MEASUREMENTS", "")


@register.simple_tag
def show_banner():
    return getattr(settings, "SHOW_BANNER", "")


@register.simple_tag
def show_je_donne_mon_avis():
    return getattr(settings, "SHOW_JE_DONNE_MON_AVIS", "")
