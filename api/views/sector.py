import logging

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView

from api.serializers import SectorSerializer
from data.models import Sector

logger = logging.getLogger(__name__)


@extend_schema_view(
    get=extend_schema(
        summary="Lister les secteurs des cantines.",
        description="Une cantine peut s'assigner un ou plusieurs secteurs d'activité.",
    ),
)
class SectorListView(ListAPIView):
    include_in_documentation = True
    required_scopes = ["canteen"]
    model = Sector
    serializer_class = SectorSerializer
    queryset = Sector.objects.all()
