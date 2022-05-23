from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.exceptions import NotFound, PermissionDenied, MethodNotAllowed
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_excel.renderers import XLSXRenderer
from drf_excel.mixins import XLSXFileMixin
from django.core.exceptions import BadRequest, ObjectDoesNotExist
from django.db.models import Sum, Q, Func, F
from django.http import JsonResponse
from django_filters import rest_framework as django_filters
from api.permissions import IsLinkedCanteenManager, IsCanteenManager, IsAuthenticated
from api.serializers import PurchaseSerializer, PurchaseSummarySerializer, PurchaseExportSerializer
from data.models import Purchase, Canteen
from .utils import CamelCaseOrderingFilter, UnaccentSearchFilter
from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)


class PurchasesPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50
    categories = []
    characteristics = []
    canteens = []

    def paginate_queryset(self, queryset, request, view=None):
        # Performance improvements possible
        user_purchases = Purchase.objects.filter(canteen__in=request.user.canteens.all())
        category_param = request.query_params.get("category")
        if category_param:
            category_qs = user_purchases
            characteristic_param = request.query_params.getlist("characteristics")
            if characteristic_param:
                category_qs = category_qs.filter(characteristics__overlap=characteristic_param)
                self.categories = set(filter(lambda x: x, category_qs.values_list("category", flat=True)))
            else:
                self.categories = list(Purchase.Category)
        else:
            self.categories = set(filter(lambda x: x, queryset.values_list("category", flat=True)))
        self.canteens = list(
            queryset.order_by("canteen__id").distinct("canteen__id").values_list("canteen__id", flat=True)
        )

        self.characteristics = []
        all_characteristics = list(Purchase.Characteristic)
        characteristic_qs = user_purchases
        if category_param:
            characteristic_qs = characteristic_qs.filter(category=category_param)
        for c in all_characteristics:
            if characteristic_qs.filter(characteristics__contains=[c]).exists():
                self.characteristics.append(c)

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                    ("categories", self.categories),
                    ("characteristics", self.characteristics),
                    ("canteens", self.canteens),
                ]
            )
        )


class PurchaseFilterSet(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Purchase
        fields = (
            "canteen__id",
            "category",
            "date",
        )


class PurchaseListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsLinkedCanteenManager]
    model = Purchase
    serializer_class = PurchaseSerializer
    pagination_class = PurchasesPagination
    filter_backends = [
        CamelCaseOrderingFilter,
        UnaccentSearchFilter,
        django_filters.DjangoFilterBackend,
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
    filterset_class = PurchaseFilterSet

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

    def filter_queryset(self, queryset):
        # handle characteristics filtering manually because ChoiceArrayField is not a Django field
        characteristics = self.request.query_params.getlist("characteristics")
        if characteristics:
            queryset = queryset.filter(characteristics__overlap=characteristics)
        return super().filter_queryset(queryset)


class PurchaseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsLinkedCanteenManager]
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


class PurchaseOptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        purchases = Purchase.objects.filter(canteen__in=self.request.user.canteens.all())
        products = list(
            purchases.filter(description__isnull=False)
            .order_by("description")
            .distinct("description")
            .values_list("description", flat=True)
        )
        providers = list(
            purchases.filter(provider__isnull=False)
            .order_by("provider")
            .distinct("provider")
            .values_list("provider", flat=True)
        )
        return JsonResponse({"products": products, "providers": providers}, status=200)
