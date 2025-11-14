import logging

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView

from api.serializers import SectorM2MSerializer
from data.models import SectorM2M

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
    model = SectorM2M
    serializer_class = SectorM2MSerializer
    queryset = SectorM2M.objects.all()
