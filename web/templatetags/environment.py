from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def environment():
    return getattr(settings, "ENVIRONMENT", "")


@register.simple_tag
def admin_css_override():
    env = getattr(settings, "ENVIRONMENT", "")
    if env == "dev":
        return "css/admin_color_dev.css"
    if env == "staging":
        return "css/admin_color_staging.css"
    if env == "demo":
        return "css/admin_color_demo.css"
    return None


@register.simple_tag
def hostname():
    protocol = "https://" if getattr(settings, "SECURE") else "http://"
    return f"{protocol}{getattr(settings, 'HOSTNAME', '')}"
