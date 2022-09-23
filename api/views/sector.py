import logging
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema_view, extend_schema
from api.serializers import SectorSerializer
from data.models import Sector

logger = logging.getLogger(__name__)


@extend_schema_view(
    get=extend_schema(
        summary="Liste les secteurs des cantines.",
        description="Une cantine peut s'assigner un ou plusieurs secteurs.",
    ),
)
class SectorListView(ListAPIView):
    include_in_documentation = True
    required_scopes = ["canteen"]
    model = Sector
    serializer_class = SectorSerializer
    queryset = Sector.objects.all()
