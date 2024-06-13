from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.exceptions import NotFound, PermissionDenied, MethodNotAllowed
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_excel.renderers import XLSXRenderer
from drf_excel.mixins import XLSXFileMixin
from django.core.exceptions import BadRequest, ObjectDoesNotExist, ValidationError
from django.db.models import Sum, Q
from django.db.models.functions import ExtractYear
from django.http import JsonResponse
from django_filters import rest_framework as django_filters
from api.permissions import IsLinkedCanteenManager, IsCanteenManager, IsAuthenticated
from api.serializers import (
    PurchaseSerializer,
    PurchaseSummarySerializer,
    PurchasePercentageSummarySerializer,
    PurchaseExportSerializer,
)
from data.models import Purchase, Canteen, Diagnostic
from .utils import MaCantineOrderingFilter, UnaccentSearchFilter
from collections import OrderedDict
import logging


logger = logging.getLogger(__name__)


class PurchasesPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50
    families = []
    characteristics = []
    canteens = []

    def paginate_queryset(self, queryset, request, view=None):
        # Performance improvements possible
        user_purchases = Purchase.objects.filter(canteen__in=request.user.canteens.all())
        family_param = request.query_params.get("family")
        if family_param:
            family_qs = user_purchases
            characteristic_param = request.query_params.getlist("characteristics")
            if characteristic_param:
                family_qs = family_qs.filter(characteristics__overlap=characteristic_param)
                self.families = set(filter(lambda x: x, family_qs.values_list("family", flat=True)))
            else:
                self.families = list(Purchase.Family)
        else:
            self.families = set(filter(lambda x: x, queryset.values_list("family", flat=True)))
        self.canteens = list(
            queryset.order_by("canteen__id").distinct("canteen__id").values_list("canteen__id", flat=True)
        )

        self.characteristics = []
        all_characteristics = list(Purchase.Characteristic)
        characteristic_qs = user_purchases
        if family_param:
            characteristic_qs = characteristic_qs.filter(family=family_param)
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
                    ("families", self.families),
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
            "family",
            "date",
        )


class PurchaseListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsLinkedCanteenManager]
    model = Purchase
    serializer_class = PurchaseSerializer
    pagination_class = PurchasesPagination
    filter_backends = [
        MaCantineOrderingFilter,
        UnaccentSearchFilter,
        django_filters.DjangoFilterBackend,
    ]
    ordering_fields = [
        "creation_date",
        "date",
        "provider",
        "price_ht",
        "canteen__name",
        "description",
        "family",
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
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        canteen_id = kwargs.get("canteen_pk")
        canteen = self._get_canteen(canteen_id, self.request)
        year = request.query_params.get("year")
        data = canteen_summary_for_year(canteen, year) if year else canteen_summary(canteen)
        return Response(PurchaseSummarySerializer(data).data if year else data)

    def _get_canteen(self, canteen_id, request):
        try:
            canteen = Canteen.objects.get(pk=canteen_id)
            if not IsCanteenManager().has_object_permission(request, self, canteen):
                raise PermissionDenied()
            return canteen
        except Canteen.DoesNotExist as e:
            raise NotFound() from e


class CanteenPurchasesPercentageSummaryView(APIView):
    def get(self, request, *args, **kwargs):
        canteen_id = kwargs.get("canteen_pk")
        canteen = self._get_canteen(canteen_id, self.request)
        year = request.query_params.get("year")
        try:
            year = int(year)
        except ValueError:
            raise BadRequest("an integer is required for the year query parameter")
        except TypeError:
            raise BadRequest("the year query parameter is required")

        is_canteen_manager = IsCanteenManager().has_object_permission(request, self, canteen)
        ignore_redaction = is_canteen_manager and request.query_params.get("ignoreRedaction") == "true"
        if not ignore_redaction and year in canteen.redacted_appro_years:
            raise NotFound()

        data = canteen_summary_for_year(canteen, year)
        if data["value_total_ht"] == 0:
            raise NotFound()

        if is_canteen_manager:
            data["last_purchase_date"] = (
                Purchase.objects.only("date").filter(canteen=canteen, date__year=year).latest("date").date
            )

        return Response(PurchasePercentageSummarySerializer(data).data)

    def _get_canteen(self, canteen_id, request):
        try:
            canteen = Canteen.objects.get(pk=canteen_id)
            return canteen
        except Canteen.DoesNotExist as e:
            raise NotFound() from e


def canteen_summary_for_year(canteen, year):
    purchases = Purchase.objects.only("id", "family", "characteristics", "price_ht").filter(
        canteen=canteen, date__year=year
    )
    data = {"year": year}
    simple_diag_data(purchases, data)
    complete_diag_data(purchases, data)
    misc_totals(purchases, data)

    return data


def canteen_summary(canteen):
    data = {"results": []}
    years = (
        Purchase.objects.filter(canteen=canteen).annotate(year=ExtractYear("date")).order_by("year").distinct("year")
    )
    years = [y["year"] for y in years.values()]
    for year in years:
        year_data = {"year": year}
        purchases = Purchase.objects.only("id", "family", "characteristics", "price_ht").filter(
            canteen=canteen, date__year=year
        )
        simple_diag_data(purchases, year_data)
        data["results"].append(year_data)

    return data


# the order of EGALIM_LABELS is significant - determines which labels trump others when aggregating purchases
DIAGNOSTIC_EGALIM_LABELS = [
    "BIO",
    "LABEL_ROUGE",
    "AOCAOP_IGP_STG",
    "HVE",
    "PECHE_DURABLE",
    "RUP",
    "COMMERCE_EQUITABLE",
    "FERMIER",
    "EXTERNALITES",
    "PERFORMANCE",
]
PURCHASE_EGALIM_LABELS = [
    "BIO",
    "LABEL_ROUGE",
    "AOCAOP",
    "IGP",
    "STG",
    "HVE",
    "PECHE_DURABLE",
    "RUP",
    "COMMERCE_EQUITABLE",
    "FERMIER",
    "EXTERNALITES",
    "PERFORMANCE",
    "EQUIVALENTS",
]


def simple_diag_data(purchases, data):
    # TODO: is CONVERSION_BIO used?
    bio_filter = Q(characteristics__contains=[Purchase.Characteristic.BIO]) | Q(
        characteristics__contains=[Purchase.Characteristic.CONVERSION_BIO]
    )
    siqo_filter = (
        Q(characteristics__contains=[Purchase.Characteristic.LABEL_ROUGE])
        | Q(characteristics__contains=[Purchase.Characteristic.AOCAOP])
        | Q(characteristics__contains=[Purchase.Characteristic.IGP])
        | Q(characteristics__contains=[Purchase.Characteristic.STG])
    )
    egalim_others_filter = (
        Q(characteristics__contains=[Purchase.Characteristic.HVE])
        | Q(characteristics__contains=[Purchase.Characteristic.PECHE_DURABLE])
        | Q(characteristics__contains=[Purchase.Characteristic.RUP])
        | Q(characteristics__contains=[Purchase.Characteristic.FERMIER])
        | Q(characteristics__contains=[Purchase.Characteristic.COMMERCE_EQUITABLE])
    )
    externalities_performance_filter = Q(characteristics__contains=[Purchase.Characteristic.EXTERNALITES]) | Q(
        characteristics__contains=[Purchase.Characteristic.PERFORMANCE]
    )

    data["value_total_ht"] = purchases.aggregate(total=Sum("price_ht"))["total"] or 0
    bio_purchases = purchases.filter(bio_filter).distinct()
    data["value_bio_ht"] = bio_purchases.aggregate(total=Sum("price_ht"))["total"] or 0

    # the remaining stats should ignore any bio products
    purchases_no_bio = purchases.exclude(bio_filter)
    siqo_purchases = purchases_no_bio.filter(siqo_filter).distinct()
    data["value_sustainable_ht"] = siqo_purchases.aggregate(total=Sum("price_ht"))["total"] or 0

    # the remaining stats should ignore any SIQO products
    purchases_no_siqo = purchases_no_bio.exclude(siqo_filter)
    egalim_others_purchases = purchases_no_siqo.filter(egalim_others_filter).distinct()
    data["value_egalim_others_ht"] = egalim_others_purchases.aggregate(total=Sum("price_ht"))["total"] or 0

    # the remaining stats should ignore any "other Egalim" products
    purchases_no_other = purchases_no_siqo.exclude(egalim_others_filter)
    externalities_performance_purchases = purchases_no_other.filter(externalities_performance_filter).distinct()
    data["value_externality_performance_ht"] = (
        externalities_performance_purchases.aggregate(total=Sum("price_ht"))["total"] or 0
    )


def complete_diag_data(purchases, data):
    # summary for detailed teledeclaration totals, by family and label
    families = [
        "VIANDES_VOLAILLES",
        "PRODUITS_DE_LA_MER",
        "FRUITS_ET_LEGUMES",
        "CHARCUTERIE",
        "PRODUITS_LAITIERS",
        "BOULANGERIE",
        "BOISSONS",
        "AUTRES",
    ]
    other_labels = ["FRANCE", "SHORT_DISTRIBUTION", "LOCAL"]

    for family in families:
        purchase_family = purchases.filter(family=family)
        for label in DIAGNOSTIC_EGALIM_LABELS:
            if label == "AOCAOP_IGP_STG":
                fam_label = purchase_family.filter(
                    Q(characteristics__contains=[Purchase.Characteristic.AOCAOP])
                    | Q(characteristics__contains=[Purchase.Characteristic.IGP])
                    | Q(characteristics__contains=[Purchase.Characteristic.STG])
                ).distinct()
                # the remaining stats should ignore already counted labels
                purchase_family = purchase_family.exclude(
                    Q(characteristics__contains=[Purchase.Characteristic.AOCAOP])
                    | Q(characteristics__contains=[Purchase.Characteristic.IGP])
                    | Q(characteristics__contains=[Purchase.Characteristic.STG])
                )
            else:
                fam_label = purchase_family.filter(Q(characteristics__contains=[Purchase.Characteristic[label]]))
                # the remaining stats should ignore already counted labels
                purchase_family = purchase_family.exclude(
                    Q(characteristics__contains=[Purchase.Characteristic[label]])
                )
            key = "value_" + family.lower() + "_" + label.lower()
            data[key] = fam_label.aggregate(total=Sum("price_ht"))["total"] or 0
        # outside of EGAlim, products can be counted twice across characteristics
        purchase_family = purchases.filter(family=family)
        other_labels_characteristics = []
        for label in other_labels:
            characteristic = Purchase.Characteristic[label]
            fam_label = purchase_family.filter(Q(characteristics__contains=[characteristic]))
            key = "value_" + family.lower() + "_" + label.lower()
            data[key] = fam_label.aggregate(total=Sum("price_ht"))["total"] or 0
            other_labels_characteristics.append(characteristic)
        # Non-EGAlim totals: contains no labels or only one or more of other_labels
        non_egalim_purchases = purchase_family.filter(
            Q(characteristics__contained_by=(other_labels_characteristics + [""])) | Q(characteristics__len=0)
        ).distinct()
        key = "value_" + family.lower() + "_non_egalim"
        data[key] = non_egalim_purchases.aggregate(total=Sum("price_ht"))["total"] or 0


def misc_totals(purchases, data):
    meat_poultry_purchases = purchases.filter(
        family=Purchase.Family.VIANDES_VOLAILLES,
    )
    data["value_meat_poultry_ht"] = meat_poultry_purchases.aggregate(total=Sum("price_ht"))["total"] or 0

    meat_poultry_egalim = meat_poultry_purchases.filter(characteristics__overlap=PURCHASE_EGALIM_LABELS)
    data["value_meat_poultry_egalim_ht"] = meat_poultry_egalim.aggregate(total=Sum("price_ht"))["total"] or 0

    meat_poultry_france = meat_poultry_purchases.filter(
        characteristics__contains=[
            "FRANCE",
        ]
    )
    data["value_meat_poultry_france_ht"] = meat_poultry_france.aggregate(total=Sum("price_ht"))["total"] or 0

    fish_purchases = purchases.filter(
        family=Purchase.Family.PRODUITS_DE_LA_MER,
    )
    data["value_fish_ht"] = fish_purchases.aggregate(total=Sum("price_ht"))["total"] or 0

    fish_egalim = fish_purchases.filter(characteristics__overlap=PURCHASE_EGALIM_LABELS)
    data["value_fish_egalim_ht"] = fish_egalim.aggregate(total=Sum("price_ht"))["total"] or 0


class DiagnosticsFromPurchasesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        year = kwargs.get("year")
        canteen_ids = request.data.get("canteen_ids")
        if not year or not canteen_ids:
            raise BadRequest("Missing year and/or canteen ids")

        created_diags = []
        errors = []
        for canteen_id in canteen_ids:
            try:
                canteen = Canteen.objects.get(id=canteen_id)
            except Canteen.DoesNotExist:
                errors.append(f"Cantine inconnue : {canteen_id}")
                continue
            if request.user not in canteen.managers.all():
                errors.append(f"Vous ne gérez pas la cantine : {canteen_id}")
                continue
            values_dict = canteen_summary_for_year(canteen, year)
            total_ht = values_dict["value_total_ht"]
            if total_ht == 0 or total_ht is None:
                errors.append(f"Aucun achat trouvé pour la cantine : {canteen_id}")
                continue
            if canteen.is_central_cuisine:
                values_dict["central_kitchen_diagnostic_mode"] = Diagnostic.CentralKitchenDiagnosticMode.APPRO
            diagnostic = Diagnostic(
                canteen=canteen, year=year, diagnostic_type=Diagnostic.DiagnosticType.COMPLETE, **values_dict
            )
            try:
                diagnostic.full_clean()
            except ValidationError:
                errors.append(f"Il existe déjà un diagnostic pour l'année {year} pour la cantine : {canteen_id}")
                continue
            diagnostic.save()
            created_diags.append(diagnostic.id)
        return JsonResponse({"results": created_diags, "errors": errors}, status=status.HTTP_201_CREATED)


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
            "Famille de produit",
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


class PurchasesDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        purchase_ids = request.data.get("ids")
        purchases = Purchase.objects.filter(canteen__in=self.request.user.canteens.all(), id__in=purchase_ids)
        deleted_count = purchases.delete()
        return JsonResponse({"count": deleted_count}, status=status.HTTP_200_OK)


class PurchasesRestoreView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        purchase_ids = request.data.get("ids")
        purchases_to_restore = Purchase.all_objects.filter(
            canteen__in=self.request.user.canteens.all(), id__in=purchase_ids
        )
        restored_count = purchases_to_restore.update(deletion_date=None)
        return JsonResponse({"count": restored_count}, status=status.HTTP_200_OK)
