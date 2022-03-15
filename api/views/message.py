import logging
from data.models import Message
from api.serializers import MessageSerializer
from django.conf import settings
from rest_framework.generics import CreateAPIView
from common.utils import send_mail

logger = logging.getLogger(__name__)


class MessageCreateView(CreateAPIView):
    model = Message
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        create = super().perform_create(serializer)
        data = serializer.validated_data
        send_mail(
            subject="📨 Nouveau message en attente de validation",
            template="pending_message",
            context={
                "sender_email": data["sender_email"],
                "sender_name": data.get("sender_name") or "Pas renseigné",
                "canteen_name": data["destination_canteen"].name,
                "body": data["body"],
            },
            to=[settings.CONTACT_EMAIL],
        )
        return create
