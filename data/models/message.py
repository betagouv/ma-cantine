import logging
from django.db import models
from data.models import Canteen
from django.conf import settings
from common.utils import send_mail
from django.utils.timezone import now

logger = logging.getLogger(__name__)


class Message(models.Model):
    class Meta:
        ordering = ["-creation_date"]

    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente de validation"
        SENT = "SENT", "Envoyé"
        BLOCKED = "BLOCKED", "Bloqué"

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    destination_canteen = models.ForeignKey(
        Canteen, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="destinataire"
    )
    sender_name = models.TextField(null=True, blank=True, verbose_name="nom de l'expéditeur")
    sender_email = models.TextField(verbose_name="adresse email de l'expéditeur")
    body = models.TextField(verbose_name="message")

    status = models.CharField(max_length=255, choices=Status.choices, default=Status.PENDING, verbose_name="État")

    sent_date = models.DateField(null=True, blank=True)

    def send(self):
        if self.status == Message.Status.SENT:
            logger.exception(f"Attempt to send an already sent message: {self.id}")
            raise Exception(f"Message already sent on {self.sent_date}")
        recipients = [user.email for user in self.destination_canteen.managers.all()]
        recipients.append(settings.CONTACT_EMAIL)
        reply_to = [self.sender_email]

        context = {
            "canteen": self.destination_canteen.name,
            "from": self.sender_email,
            "name": self.sender_name or "Une personne",
            "message": self.body,
        }

        try:
            send_mail(
                subject=f"Un message pour {self.destination_canteen.name}",
                to=recipients,
                reply_to=reply_to,
                template="contact_canteen",
                context=context,
            )
            self.status = Message.Status.SENT
            self.sent_date = now()
            self.save()
        except Exception as e:
            logger.exception(f"Error sending message {self.id}:\n{e}")

    def block(self):
        if self.status == Message.Status.SENT:
            logger.exception(f"Attempt to block an already sent message: {self.id}")
            raise Exception(f"Cannot block message already sent on {self.sent_date}")
        self.status = Message.Status.BLOCKED
        self.save()

    def __str__(self):
        return f"Message envoyé de {self.sender_email} à {self.destination_canteen.name}"
