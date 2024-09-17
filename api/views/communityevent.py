from django.utils import timezone
from rest_framework.generics import ListAPIView

from api.serializers import CommunityEventSerializer
from data.models import CommunityEvent


class CommunityEventsView(ListAPIView):
    model = CommunityEvent
    serializer_class = CommunityEventSerializer
    queryset = CommunityEvent.objects.filter(end_date__gt=timezone.now())
