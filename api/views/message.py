import logging

from rest_framework.generics import CreateAPIView

from api.serializers import MessageSerializer
from data.models import Message

logger = logging.getLogger(__name__)


class MessageCreateView(CreateAPIView):
    model = Message
    serializer_class = MessageSerializer
