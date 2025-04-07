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
def teledeclaration_correction_campaign():
    return getattr(settings, "TELEDECLARATION_CORRECTION_CAMPAIGN", "")


@register.simple_tag
def enable_dashboard():
    return getattr(settings, "ENABLE_DASHBOARD", "")


@register.simple_tag
def enable_waste_measurements():
    return getattr(settings, "ENABLE_WASTE_MEASUREMENTS", "")


@register.simple_tag
def show_management_information_banner():
    return getattr(settings, "SHOW_MANAGEMENT_INFORMATION_BANNER", "")
