import base64
import logging

import html2text
import redis as r
import requests
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

redis = r.from_url(settings.REDIS_URL, decode_responses=True)


def get_token_sirene():
    if not settings.SIRET_API_KEY or not settings.SIRET_API_SECRET:
        logger.warning("skipping siret token fetching because key and secret env vars aren't set")
        return
    token_redis_key = f"{settings.REDIS_PREPEND_KEY}SIRET_API_TOKEN"
    if redis.exists(token_redis_key):
        return redis.get(token_redis_key)

    base64Cred = base64.b64encode(bytes(f"{settings.SIRET_API_KEY}:{settings.SIRET_API_SECRET}", "utf-8")).decode(
        "utf-8"
    )
    token_data = {"grant_type": "client_credentials", "validity_period": 604800}
    token_headers = {"Authorization": f"Basic {base64Cred}"}
    token_response = requests.post("https://api.insee.fr/token", data=token_data, headers=token_headers)
    if token_response.ok:
        token_response = token_response.json()
        token = token_response["access_token"]
        expiration_seconds = 60 * 60 * 24
        redis.set(token_redis_key, token, ex=expiration_seconds)
        return token
    else:
        logger.warning(f"token fetching failed, code {token_response.status_code} : {token_response}")


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
    subject = kwargs.pop("subject")
    env = getattr(settings, "ENVIRONMENT", "")
    if env == "demo" or env == "staging":
        subject = f"({env.upper()}) {subject}"
    message = EmailMultiAlternatives(**kwargs, subject=subject, body=text_content)
    if html_content:
        message.attach_alternative(html_content, "text/html")
    message.send(fail_silently=fail_silently)


def _add_additional_context(context, **kwargs):
    reply_to = kwargs.get("reply_to") or kwargs.get("from")
    replies_to_team = True
    if reply_to and reply_to != [settings.CONTACT_EMAIL]:
        replies_to_team = False
    context["repliesToTeam"] = replies_to_team
    if "us" not in context:
        context["us"] = settings.DEFAULT_FROM_EMAIL
