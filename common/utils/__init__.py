from django.core.mail import send_mail as django_send_mail
from django.core.mail import EmailMultiAlternatives


def send_mail(*args, **kwargs):
    if kwargs.get("reply_to"):
        html_content = kwargs.pop("html_content")
        message = EmailMultiAlternatives(*args, **kwargs)
        message.attach_alternative(html_content, "text/html")
        message.send()
    else:
        django_send_mail(*args, **kwargs)
