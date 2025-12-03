import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django_filters import rest_framework as django_filters
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from drf_spectacular.utils import extend_schema, extend_schema_view
from api.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrTokenHasResourceScope,
    IsCanteenManager,
    IsLinkedCanteenManager,
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
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope]
    model = WasteMeasurement
    serializer_class = WasteMeasurementSerializer
    filter_backends = [
        django_filters.DjangoFilterBackend,
    ]
    filterset_class = WasteMeasurementFilterSet

    def _get_canteen(self):
        canteen_id = self.request.parser_context.get("kwargs").get("canteen_pk")
        try:
            canteen = Canteen.objects.get(pk=canteen_id)
        except ObjectDoesNotExist as e:
            logger.warning(
                f"Attempt to create/view a waste measurement from an unexistent canteen ID : {canteen_id}: \n{e}"
            )
            raise NotFound()

        if not IsCanteenManager().has_object_permission(self.request, self, canteen):
            raise PermissionDenied()

        return canteen

    def get_queryset(self):
        canteen = self._get_canteen()
        return WasteMeasurement.objects.filter(canteen=canteen).order_by("-period_start_date")

    def perform_create(self, serializer):
        canteen = self._get_canteen()
        serializer.is_valid(raise_exception=True)
        measurement = serializer.save(canteen=canteen)
        update_change_reason_with_auth(self, measurement)


class CanteenWasteMeasurementView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsLinkedCanteenManager]
    queryset = WasteMeasurement.objects.all()
    serializer_class = WasteMeasurementSerializer

    def put(self, request, *args, **kwargs):
        return JsonResponse(
            {"error": "Only PATCH request supported in this resource"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
