from rest_framework.generics import ListAPIView

from api.serializers import CommunityEventSerializer
from data.models import CommunityEvent


class CommunityEventsView(ListAPIView):
    model = CommunityEvent
    serializer_class = CommunityEventSerializer

    def get_queryset(self):
        return CommunityEvent.objects.upcoming()
