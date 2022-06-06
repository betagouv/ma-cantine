from api.serializers import CommunityEventSerializer
from data.models import CommunityEvent
from django.utils import timezone
from rest_framework.generics import ListAPIView


class CommunityEventsView(ListAPIView):
    model = CommunityEvent
    serializer_class = CommunityEventSerializer
    queryset = CommunityEvent.objects.filter(date__gte=timezone.now())
