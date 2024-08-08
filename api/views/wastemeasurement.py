import logging
from data.models import WasteMeasurement
from api.serializers import WasteMeasurementSerializer

# from django.conf import settings
# from django.db import IntegrityError
# from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, HttpResponseServerError
# from django.core.exceptions import ObjectDoesNotExist, ValidationError
# from drf_spectacular.utils import extend_schema_view, extend_schema
# from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import CreateAPIView  # ,UpdateAPIView,  ListAPIView

# from rest_framework.exceptions import NotFound, PermissionDenied
# from rest_framework.views import APIView
# from api.serializers import ManagerWasteMeasurementSerializer, WasteMeasurementAndCanteenSerializer
# from api.views.utils import update_change_reason_with_auth
from data.models import Canteen  # , Teledeclaration

from api.permissions import (
    IsAuthenticated,
    IsCanteenManager,
)

# from api.exceptions import DuplicateException
from api.views.utils import update_change_reason_with_auth
from django.core.exceptions import ObjectDoesNotExist  # , ValidationError
from rest_framework.exceptions import NotFound, PermissionDenied

logger = logging.getLogger(__name__)


class WasteMeasurementCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    model = WasteMeasurement
    serializer_class = WasteMeasurementSerializer

    def perform_create(self, serializer):
        try:
            canteen_id = self.request.parser_context.get("kwargs").get("canteen_pk")
            canteen = Canteen.objects.get(pk=canteen_id)
            if not IsCanteenManager().has_object_permission(self.request, self, canteen):
                raise PermissionDenied()
            serializer.is_valid(raise_exception=True)
            diagnostic = serializer.save(canteen=canteen)
            update_change_reason_with_auth(self, diagnostic)
        except ObjectDoesNotExist as e:
            logger.warning(
                f"Attempt to create a waste measurement from an unexistent canteen ID : {canteen_id}: \n{e}"
            )
            raise NotFound()
