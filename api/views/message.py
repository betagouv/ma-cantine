import logging
from data.models import Message
from api.serializers import MessageSerializer
from rest_framework.generics import CreateAPIView

logger = logging.getLogger(__name__)


class MessageCreateView(CreateAPIView):
    model = Message
    serializer_class = MessageSerializer
