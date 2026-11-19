import logging

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import PartnerTypeSerializer
from data.models import PartnerType

logger = logging.getLogger(__name__)


@extend_schema_view(
    get=extend_schema(
        summary="Lister les types d'acteur des partenaires.",
        description="Un partenaire peut avoir un ou plusieurs types d'acteur.",
    ),
)
class PartnerTypeListView(APIView):
    @extend_schema(responses=PartnerTypeSerializer(many=True))
    def get(self, request, format=None):
        partner_types = [{"id": partner_type.value, "name": partner_type.label} for partner_type in PartnerType]
        return Response(PartnerTypeSerializer(partner_types, many=True).data)
