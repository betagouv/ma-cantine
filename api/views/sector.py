import logging

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.response import Response
from rest_framework.views import APIView

from data.models.sector import Sector, get_sector_category_from_sector, is_sector_with_line_ministry
from api.serializers.sector import SectorSerializer

logger = logging.getLogger(__name__)


@extend_schema_view(
    get=extend_schema(
        summary="Lister les secteurs des cantines.",
        description="Une cantine peut s'assigner un ou plusieurs secteurs d'activité.",
    ),
)
class SectorListView(APIView):
    include_in_documentation = True

    @extend_schema(responses=SectorSerializer(many=True))
    def get(self, request, format=None):
        sectors = []
        for sector in Sector:
            sector_category = get_sector_category_from_sector(sector)
            sectors.append(
                {
                    "value": sector.value,
                    "name": sector.label,
                    "category": sector_category.value,
                    "category_name": sector_category.label,
                    "has_line_ministry": is_sector_with_line_ministry(sector),
                }
            )
        return Response(SectorSerializer(sectors, many=True).data)
