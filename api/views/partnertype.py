import logging
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema_view, extend_schema
from api.serializers import PartnerTypeSerializer
from data.models import PartnerType

logger = logging.getLogger(__name__)


@extend_schema_view(
    get=extend_schema(
        summary="Lister les secteurs des cantines.",
        description="Une cantine peut s'assigner un ou plusieurs secteurs d'activité.",
    ),
)
class PartnerTypeListView(ListAPIView):
    model = PartnerType
    serializer_class = PartnerTypeSerializer
    queryset = PartnerType.objects.all()
