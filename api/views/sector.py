import logging
from rest_framework.generics import ListAPIView
from api.serializers import SectorSerializer
from data.models import Sector

logger = logging.getLogger(__name__)


class SectorListView(ListAPIView):
    model = Sector
    serializer_class = SectorSerializer
    queryset = Sector.objects.all()
