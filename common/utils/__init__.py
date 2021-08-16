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
    message = EmailMultiAlternatives(**kwargs, body=text_content)
    if html_content:
        message.attach_alternative(html_content, "text/html")
    message.send()


def _add_additional_context(context, **kwargs):
    reply_to = kwargs.get("reply_to") or kwargs.get("from")
    replies_to_team = True
    if reply_to and reply_to != [settings.CONTACT_EMAIL]:
        replies_to_team = False
    context["repliesToTeam"] = replies_to_team


def siret_luhn(siret):
    """
    Performs length and Luhn validation
    (https://portal.hardis-group.com/pages/viewpage.action?pageId=120357227)
    """
    if siret is None or siret == "":
        return
    if len(siret) != 14:
        return "14 caractères numériques sont attendus"
    odd_digits = [int(n) for n in siret[-1::-2]]
    even_digits = [int(n) for n in siret[-2::-2]]
    checksum = sum(odd_digits)
    for digit in even_digits:
        checksum += sum(int(n) for n in str(digit * 2))
    luhn_checksum_valid = checksum % 10 == 0

    if not luhn_checksum_valid:
        return "Le numéro SIRET n'est pas valide."
