from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from api.permissions import (
    IsAuthenticatedOrTokenHasResourceScope,
    IsCanteenManagerUrlParam,
)

from data.models import Canteen
from api.serializers import SatelliteCanteenSerializer


@extend_schema_view(
    get=extend_schema(summary="Lister les restaurants satellites d'un groupe."),
)
class CanteenGroupeSatellitesView(ListAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    # required_scopes = ["canteen"]
    model = Canteen
    serializer_class = SatelliteCanteenSerializer

    def get_queryset(self):
        canteen_pk = self.kwargs["canteen_pk"]
        return Canteen.objects.filter(groupe_id=canteen_pk)
