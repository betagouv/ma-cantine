from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework import permissions
from rest_framework.exceptions import NotFound, PermissionDenied, MethodNotAllowed
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_excel.renderers import XLSXRenderer
from drf_excel.mixins import XLSXFileMixin
from django.core.exceptions import BadRequest, ObjectDoesNotExist
from django.db.models import Sum, Q, Func, F
from django.http import JsonResponse
from api.permissions import IsLinkedCanteenManager, IsCanteenManager
from api.serializers import PurchaseSerializer, PurchaseSummarySerializer, PurchaseExportSerializer
from data.models import Purchase, Canteen
from .utils import CamelCaseOrderingFilter, UnaccentSearchFilter
import logging

logger = logging.getLogger(__name__)


class PurchasesPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class PurchaseListCreateView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsLinkedCanteenManager]
    model = Purchase
    serializer_class = PurchaseSerializer
    pagination_class = PurchasesPagination
    filter_backends = [
        CamelCaseOrderingFilter,
        UnaccentSearchFilter,
    ]
    ordering_fields = [
        "date",
        "provider",
        "price_ht",
        "canteen__name",
        "description",
    ]
    search_fields = [
        "description",
        "provider",
    ]

    def get_queryset(self):
        return Purchase.objects.filter(canteen__in=self.request.user.canteens.all())

    def perform_create(self, serializer):
        canteen_id = self.request.data.get("canteen")
        if not canteen_id:
            logger.error("Canteen ID missing in purchase creation request")
            raise BadRequest("Canteen ID missing in purchase creation request")
        try:
            canteen = Canteen.objects.get(pk=canteen_id)
            if not canteen.managers.filter(pk=self.request.user.pk).exists():
                logger.error(
                    f"User {self.request.user.id} attempted to create a purchase in someone else's canteen: {canteen_id}"
                )
                raise PermissionDenied()
            serializer.save(canteen=canteen)
        except ObjectDoesNotExist as e:
            logger.error(
                f"User {self.request.user.id} attempted to create a purchase in nonexistent canteen {canteen_id}"
            )
            raise NotFound() from e


class PurchaseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsLinkedCanteenManager]
    model = Purchase
    serializer_class = PurchaseSerializer

    def put(self, request, *args, **kwargs):
        return JsonResponse({"error": "Only PATCH request supported in this resource"}, status=405)

    def get_queryset(self):
        return Purchase.objects.filter(canteen__in=self.request.user.canteens.all())

    def perform_update(self, serializer):
        canteen_id = self.request.data.get("canteen")
        if not canteen_id:
            return serializer.save()
        try:
            canteen = Canteen.objects.get(pk=canteen_id)
            if not canteen.managers.filter(pk=self.request.user.pk).exists():
                logger.error(
                    f"User {self.request.user.id} attempted to update a purchase to someone else's canteen : {canteen_id}"
                )
                raise PermissionDenied()
            serializer.save(canteen=canteen)
        except ObjectDoesNotExist as e:
            logger.error(
                f"User {self.request.user.id} attempted to update a purchase to an nonexistent canteen {canteen_id}"
            )
            raise NotFound() from e


class CanteenPurchasesSummaryView(APIView):
    def get(self, request, *args, **kwargs):
        canteen_id = kwargs.get("canteen_pk")
        year = request.query_params.get("year")
        if not year:
            raise BadRequest("Missing year in request's query parameters")

        canteen = self._get_canteen(canteen_id, request)
        purchases = Purchase.objects.filter(canteen=canteen, date__year=year)

        data = {}
        data["total"] = purchases.aggregate(total=Sum("price_ht"))["total"]
        bio_purchases = purchases.filter(
            Q(characteristics__contains=[Purchase.Characteristic.BIO])
            | Q(characteristics__contains=[Purchase.Characteristic.CONVERSION_BIO])
        ).distinct()
        data["bio"] = bio_purchases.aggregate(total=Sum("price_ht"))["total"]
        # the remaining stats should ignore any bio products
        purchases = purchases.exclude(
            Q(characteristics__contains=[Purchase.Characteristic.BIO])
            | Q(characteristics__contains=[Purchase.Characteristic.CONVERSION_BIO])
        )
        sustainable_purchases = purchases.annotate(
            characteristics_len=Func(F("characteristics"), function="CARDINALITY")
        )
        sustainable_purchases = sustainable_purchases.filter(characteristics_len__gt=0)
        data["sustainable"] = sustainable_purchases.aggregate(total=Sum("price_ht"))["total"]
        hve_purchases = purchases.filter(characteristics__contains=[Purchase.Characteristic.HVE])
        data["hve"] = hve_purchases.aggregate(total=Sum("price_ht"))["total"]
        aoc_aop_igp_purchases = purchases.filter(
            Q(characteristics__contains=[Purchase.Characteristic.AOCAOP])
            | Q(characteristics__contains=[Purchase.Characteristic.IGP])
        ).distinct()
        data["aoc_aop_igp"] = aoc_aop_igp_purchases.aggregate(total=Sum("price_ht"))["total"]
        rouge_purchases = purchases.filter(characteristics__contains=[Purchase.Characteristic.LABEL_ROUGE])
        data["rouge"] = rouge_purchases.aggregate(total=Sum("price_ht"))["total"]

        return Response(PurchaseSummarySerializer(data).data)

    def _get_canteen(self, canteen_id, request):
        try:
            canteen = Canteen.objects.get(pk=canteen_id)
            if not IsCanteenManager().has_object_permission(request, self, canteen):
                raise PermissionDenied()
            return canteen
        except Canteen.DoesNotExist as e:
            raise NotFound() from e


class PurchaseListExportView(PurchaseListCreateView, XLSXFileMixin):
    renderer_classes = (XLSXRenderer,)
    pagination_class = None
    serializer_class = PurchaseExportSerializer

    column_header = {
        "titles": [
            "Date",
            "Cantine",
            "Description",
            "Fournisseur",
            "Catégorie",
            "Caractéristiques",
            "Prix HT",
        ],
        "column_width": [18, 25, 25, 20, 35, 35, 10],
        "style": {
            "font": {
                "bold": True,
            },
        },
    }
    body = {
        "style": {
            "alignment": {
                "horizontal": "left",
                "vertical": "center",
            },
        },
        "height": 20,
    }

    def post(self, request, *args, **kwargs):
        raise MethodNotAllowed()
