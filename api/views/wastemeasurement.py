import logging
from data.models import WasteMeasurement
from api.serializers import WasteMeasurementSerializer
from rest_framework.generics import ListCreateAPIView
from data.models import Canteen
from api.permissions import (
    IsAuthenticated,
    IsCanteenManager,
)
from api.views.utils import update_change_reason_with_auth
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import NotFound, PermissionDenied

logger = logging.getLogger(__name__)


class CanteenWasteMeasurementsView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    model = WasteMeasurement
    serializer_class = WasteMeasurementSerializer

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
