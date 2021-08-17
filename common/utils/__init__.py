from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import html2text


def send_mail(**kwargs):
    html_content = None
    if kwargs.get("template"):
        template = kwargs.pop("template")
        context = kwargs.pop("context")
        _add_additional_context(context, **kwargs)
        html_content = render_to_string(f"{template}.html", context)

        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.ignore_emphasis = True
        text_content = text_maker.handle(html_content)
    else:
        text_content = kwargs.pop("message")
    fail_silently = kwargs.pop("fail_silently", False)
    message = EmailMultiAlternatives(**kwargs, body=text_content)
    if html_content:
        message.attach_alternative(html_content, "text/html")
    message.send(fail_silently=fail_silently)


def _add_additional_context(context, **kwargs):
    reply_to = kwargs.get("reply_to") or kwargs.get("from")
    replies_to_team = True
    if reply_to and reply_to != [settings.CONTACT_EMAIL]:
        replies_to_team = False
    context["repliesToTeam"] = replies_to_team
