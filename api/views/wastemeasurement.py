import logging

from django_filters import rest_framework as django_filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, get_object_or_404

from api.permissions import (
    IsAuthenticatedOrTokenHasResourceScope,
    IsCanteenManagerUrlParam,
)
from api.serializers import WasteMeasurementSerializer
from api.views.utils import update_change_reason_with_auth
from data.models import Canteen, WasteMeasurement

logger = logging.getLogger(__name__)


class WasteMeasurementFilterSet(django_filters.FilterSet):
    period_start_date = django_filters.DateFromToRangeFilter()
    period_end_date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = WasteMeasurement
        fields = (
            "period_start_date",
            "period_end_date",
        )


@extend_schema_view(
    post=extend_schema(
        summary="Créer une nouvelle évaluation du gaspillage alimentaire.",
        description="Une évaluation doit être rattachée à une cantine.",
    )
)
class CanteenWasteMeasurementsView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    queryset = WasteMeasurement.objects.none()
    serializer_class = WasteMeasurementSerializer
    filter_backends = [
        django_filters.DjangoFilterBackend,
    ]
    filterset_class = WasteMeasurementFilterSet

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def get_queryset(self):
        canteen = self._get_canteen()
        return WasteMeasurement.objects.filter(canteen=canteen).order_by("-period_start_date")

    def perform_create(self, serializer):
        canteen = self._get_canteen()
        serializer.is_valid(raise_exception=True)
        measurement = serializer.save(canteen=canteen)
        update_change_reason_with_auth(self, measurement)


@extend_schema_view(
    patch=extend_schema(
        summary="Modifier une évaluation du gaspillage alimentaire existante.",
        description="",
    )
)
class CanteenWasteMeasurementView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    http_method_names = ["get", "patch"]  # disable "put"
    model = WasteMeasurement
    serializer_class = WasteMeasurementSerializer

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def get_object(self):
        canteen = self._get_canteen()
        return get_object_or_404(WasteMeasurement, pk=self.kwargs["pk"], canteen=canteen)
