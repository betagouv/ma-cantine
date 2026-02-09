import logging
from collections import OrderedDict

from django.core.exceptions import BadRequest, ObjectDoesNotExist, ValidationError
from django.db.models import Q, Sum
from django.db.models.functions import ExtractYear
from django.http import JsonResponse
from django_filters import rest_framework as django_filters
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed, NotFound, PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters.utils import UnaccentSearchFilter
from api.permissions import IsAuthenticated, IsCanteenManager, IsLinkedCanteenManager
from api.serializers import (
    PurchaseExportSerializer,
    PurchasePercentageSummarySerializer,
    PurchaseSerializer,
    PurchaseSummarySerializer,
)
from data.models import Canteen, Diagnostic, Purchase
from data.models.creation_source import CreationSource

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
    characteristics = django_filters.CharFilter(method="filter_characteristics")
    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Purchase
        fields = (
            "canteen__id",
            "family",
            # "characteristics",
            # "date"
        )

    # characteristics is a ChoiceArrayField, we need a custom overlap filter
    def filter_characteristics(self, queryset, name, value):
        characteristics = self.request.query_params.getlist("characteristics")
        if characteristics:
            return queryset.filter(characteristics__overlap=characteristics)
        return queryset


class PurchaseListCreateView(ListCreateAPIView):
    include_in_documentation = True
    permission_classes = [IsAuthenticated, IsLinkedCanteenManager]
    model = Purchase
    serializer_class = PurchaseSerializer
    pagination_class = PurchasesPagination
    filter_backends = [
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
        return Purchase.objects.select_related("canteen").filter(canteen__in=self.request.user.canteens.all())

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
            serializer.is_valid(raise_exception=True)
            creation_source = serializer.validated_data.get("creation_source") or CreationSource.API
            serializer.save(canteen=canteen, creation_source=creation_source)
        except ObjectDoesNotExist as e:
            logger.error(
                f"User {self.request.user.id} attempted to create a purchase in nonexistent canteen {canteen_id}"
            )
            raise NotFound() from e


class PurchaseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsLinkedCanteenManager]
    http_method_names = ["get", "patch", "delete"]  # disable "put"
    model = Purchase
    serializer_class = PurchaseSerializer

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
        if data["valeur_totale"] == 0:
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


def simple_diag_data(purchases, data):
    # TODO: is CONVERSION_BIO used?
    bio_filter = Q(characteristics__contains=[Purchase.Characteristic.BIO]) | Q(
        characteristics__contains=[Purchase.Characteristic.CONVERSION_BIO]
    )
    bio_commerce_equitable_filter = bio_filter & Q(
        characteristics__contains=[Purchase.Characteristic.COMMERCE_EQUITABLE]
    )
    siqo_filter = (
        Q(characteristics__contains=[Purchase.Characteristic.LABEL_ROUGE])
        | Q(characteristics__contains=[Purchase.Characteristic.AOCAOP])
        | Q(characteristics__contains=[Purchase.Characteristic.IGP])
        | Q(characteristics__contains=[Purchase.Characteristic.STG])
    )
    egalim_autres_filter = (
        Q(characteristics__contains=[Purchase.Characteristic.HVE])
        | Q(characteristics__contains=[Purchase.Characteristic.PECHE_DURABLE])
        | Q(characteristics__contains=[Purchase.Characteristic.RUP])
        | Q(characteristics__contains=[Purchase.Characteristic.FERMIER])
        | Q(characteristics__contains=[Purchase.Characteristic.COMMERCE_EQUITABLE])
    )
    egalim_autres_commerce_equitable_filter = egalim_autres_filter & Q(
        characteristics__contains=[Purchase.Characteristic.COMMERCE_EQUITABLE]
    )
    externalities_performance_filter = Q(characteristics__contains=[Purchase.Characteristic.EXTERNALITES]) | Q(
        characteristics__contains=[Purchase.Characteristic.PERFORMANCE]
    )

    data["valeur_totale"] = purchases.aggregate(total=Sum("price_ht"))["total"] or 0

    bio_purchases = purchases.filter(bio_filter).distinct()
    data["valeur_bio"] = bio_purchases.aggregate(total=Sum("price_ht"))["total"] or 0
    data["valeur_bio_dont_commerce_equitable"] = (
        bio_purchases.filter(bio_commerce_equitable_filter).aggregate(total=Sum("price_ht"))["total"] or 0
    )

    # the remaining stats should ignore any bio products
    purchases_no_bio = purchases.exclude(bio_filter)
    siqo_purchases = purchases_no_bio.filter(siqo_filter).distinct()
    data["valeur_siqo"] = siqo_purchases.aggregate(total=Sum("price_ht"))["total"] or 0

    # the remaining stats should also ignore any sustainable (SIQO) products
    purchases_no_bio_no_siqo = purchases_no_bio.exclude(siqo_filter)
    egalim_autres_purchases = purchases_no_bio_no_siqo.filter(egalim_autres_filter).distinct()
    data["valeur_egalim_autres"] = egalim_autres_purchases.aggregate(total=Sum("price_ht"))["total"] or 0
    data["valeur_egalim_autres_dont_commerce_equitable"] = (
        egalim_autres_purchases.filter(egalim_autres_commerce_equitable_filter).aggregate(total=Sum("price_ht"))[
            "total"
        ]
        or 0
    )

    # the remaining stats should also ignore any "other EGalim" products
    purchases_no_bio_siqo_no_egalim_autres = purchases_no_bio_no_siqo.exclude(egalim_autres_filter)
    externalities_performance_purchases = purchases_no_bio_siqo_no_egalim_autres.filter(
        externalities_performance_filter
    ).distinct()
    data["valeur_externalites_performance"] = (
        externalities_performance_purchases.aggregate(total=Sum("price_ht"))["total"] or 0
    )


def complete_diag_data(purchases, data):
    """
    summary for detailed teledeclaration totals, by family and label
    Note: the order of Diagnostic.APPRO_LABELS_EGALIM is significant - determines which labels trump others when aggregating purchases
    """
    for family in Diagnostic.APPRO_FAMILIES:
        purchase_family = purchases.filter(family=family.upper())
        for label in Diagnostic.APPRO_LABELS_EGALIM:
            if label.upper() == "AOCAOP_IGP_STG":
                purchase_family_label = purchase_family.filter(
                    Q(characteristics__contains=[Purchase.Characteristic.AOCAOP])
                    | Q(characteristics__contains=[Purchase.Characteristic.IGP])
                    | Q(characteristics__contains=[Purchase.Characteristic.STG])
                ).distinct()
                # the remaining stats should ignore already counted labels
                purchase_family = purchase_family.exclude(
                    Q(characteristics__contains=[Purchase.Characteristic.AOCAOP])
                    | Q(characteristics__contains=[Purchase.Characteristic.IGP])
                    | Q(characteristics__contains=[Purchase.Characteristic.STG])
                ).distinct()
            else:
                purchase_family_label = purchase_family.filter(
                    Q(characteristics__contains=[Purchase.Characteristic[label.upper()]])
                ).distinct()
                # the remaining stats should ignore already counted labels
                purchase_family = purchase_family.exclude(
                    Q(characteristics__contains=[Purchase.Characteristic[label.upper()]])
                ).distinct()
            key = "valeur_" + family + "_" + label
            data[key] = purchase_family_label.aggregate(total=Sum("price_ht"))["total"] or 0
        # special case of bio_dont_commerce_equitable (products can be counted twice across characteristics)
        purchase_family = purchases.filter(family=family.upper())
        purchase_family_label = purchase_family.filter(
            Q(characteristics__contains=[Purchase.Characteristic.BIO])
            & Q(characteristics__contains=[Purchase.Characteristic.COMMERCE_EQUITABLE])
        )
        key = "valeur_" + family + "_" + "bio_dont_commerce_equitable"
        data[key] = purchase_family_label.aggregate(total=Sum("price_ht"))["total"] or 0
        # outside of EGalim (products can be counted twice across characteristics)
        purchase_family = purchases.filter(family=family.upper())
        other_labels_characteristics = []
        for label in Diagnostic.APPRO_LABELS_FRANCE:
            characteristic = Purchase.Characteristic[label.upper()]
            purchase_family_label = purchase_family.filter(Q(characteristics__contains=[characteristic]))
            key = "valeur_" + family + "_" + label
            data[key] = purchase_family_label.aggregate(total=Sum("price_ht"))["total"] or 0
            other_labels_characteristics.append(characteristic)
        # Non-EGalim totals (contains no labels or only one or more of other_labels)
        non_egalim_purchases = purchase_family.filter(
            Q(characteristics__contained_by=(other_labels_characteristics + [""])) | Q(characteristics__len=0)
        ).distinct()
        key = "valeur_" + family + "_non_egalim"
        data[key] = non_egalim_purchases.aggregate(total=Sum("price_ht"))["total"] or 0


def misc_totals(purchases, data):
    # meat_poultry
    meat_poultry_purchases = purchases.filter(family=Purchase.Family.VIANDES_VOLAILLES)
    data["valeur_viandes_volailles"] = meat_poultry_purchases.aggregate(total=Sum("price_ht"))["total"] or 0
    meat_poultry_egalim = meat_poultry_purchases.filter(
        characteristics__overlap=[label.upper() for label in Diagnostic.APPRO_LABELS_EGALIM]
    )
    data["valeur_viandes_volailles_egalim"] = meat_poultry_egalim.aggregate(total=Sum("price_ht"))["total"] or 0
    meat_poultry_france = meat_poultry_purchases.filter(characteristics__contains=[Purchase.Characteristic.FRANCE])
    data["valeur_viandes_volailles_france"] = meat_poultry_france.aggregate(total=Sum("price_ht"))["total"] or 0
    # fish
    fish_purchases = purchases.filter(family=Purchase.Family.PRODUITS_DE_LA_MER)
    data["valeur_produits_de_la_mer"] = fish_purchases.aggregate(total=Sum("price_ht"))["total"] or 0
    fish_egalim = fish_purchases.filter(
        characteristics__overlap=[label.upper() for label in Diagnostic.APPRO_LABELS_EGALIM]
    )
    data["valeur_produits_de_la_mer_egalim"] = fish_egalim.aggregate(total=Sum("price_ht"))["total"] or 0


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
            valeur_totale = values_dict["valeur_totale"]
            if valeur_totale == 0 or valeur_totale is None:
                errors.append(f"Aucun achat trouvé pour la cantine : {canteen_id}")
                continue
            if canteen.is_groupe:
                values_dict["central_kitchen_diagnostic_mode"] = Diagnostic.CentralKitchenDiagnosticMode.APPRO
            diagnostic = Diagnostic(canteen=canteen, diagnostic_type=Diagnostic.DiagnosticType.COMPLETE, **values_dict)
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
