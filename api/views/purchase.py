from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.exceptions import NotFound, PermissionDenied, MethodNotAllowed
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_excel.renderers import XLSXRenderer
from drf_excel.mixins import XLSXFileMixin
from django.conf import settings
from django.core.exceptions import BadRequest, ObjectDoesNotExist, ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Sum, Q
from django.db.models.functions import ExtractYear
from django.http import JsonResponse
from django_filters import rest_framework as django_filters
from api.permissions import IsLinkedCanteenManager, IsCanteenManager, IsAuthenticated
from api.serializers import PurchaseSerializer, PurchaseSummarySerializer, PurchaseExportSerializer
from data.models import Purchase, Canteen
from .utils import MaCantineOrderingFilter, UnaccentSearchFilter, normalise_siret
from collections import OrderedDict
import logging
import csv
import time


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
    # the order of egalim_labels is significant - determines which labels trump others when aggregating purchases
    egalim_labels = [
        "BIO",
        "LABEL_ROUGE",
        "AOCAOP_IGP_STG",
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

    def get(self, request, *args, **kwargs):
        canteen_id = kwargs.get("canteen_pk")
        canteen = self._get_canteen(canteen_id, self.request)
        year = request.query_params.get("year")
        if year:
            return CanteenPurchasesSummaryView._canteen_summary_for_year(canteen, year)
        else:
            return CanteenPurchasesSummaryView._canteen_summary(canteen)

    def _canteen_summary_for_year(canteen, year):
        purchases = Purchase.objects.only("id", "family", "characteristics", "price_ht").filter(
            canteen=canteen, date__year=year
        )
        data = {}
        CanteenPurchasesSummaryView._simple_diag_data(purchases, data)
        CanteenPurchasesSummaryView._complete_diag_data(purchases, data)
        CanteenPurchasesSummaryView._misc_totals(purchases, data)

        return Response(PurchaseSummarySerializer(data).data)

    def _canteen_summary(canteen):
        data = {"results": []}
        years = (
            Purchase.objects.filter(canteen=canteen)
            .annotate(year=ExtractYear("date"))
            .order_by("year")
            .distinct("year")
        )
        years = [y["year"] for y in years.values()]
        for year in years:
            year_data = {"year": year}
            purchases = Purchase.objects.filter(canteen=canteen, date__year=year)
            CanteenPurchasesSummaryView._simple_diag_data(purchases, year_data)
            data["results"].append(year_data)

        return Response(data)

    def _get_canteen(self, canteen_id, request):
        try:
            canteen = Canteen.objects.get(pk=canteen_id)
            if not IsCanteenManager().has_object_permission(request, self, canteen):
                raise PermissionDenied()
            return canteen
        except Canteen.DoesNotExist as e:
            raise NotFound() from e

    def _simple_diag_data(purchases, data):
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

        data["value_total_ht"] = purchases.aggregate(total=Sum("price_ht"))["total"]
        bio_purchases = purchases.filter(bio_filter).distinct()
        data["value_bio_ht"] = bio_purchases.aggregate(total=Sum("price_ht"))["total"]

        # the remaining stats should ignore any bio products
        purchases_no_bio = purchases.exclude(bio_filter)
        siqo_purchases = purchases_no_bio.filter(siqo_filter).distinct()
        data["value_sustainable_ht"] = siqo_purchases.aggregate(total=Sum("price_ht"))["total"]

        # the remaining stats should ignore any SIQO products
        purchases_no_siqo = purchases_no_bio.exclude(siqo_filter)
        egalim_others_purchases = purchases_no_siqo.filter(egalim_others_filter).distinct()
        data["value_egalim_others_ht"] = egalim_others_purchases.aggregate(total=Sum("price_ht"))["total"]

        # the remaining stats should ignore any "other Egalim" products
        purchases_no_other = purchases_no_siqo.exclude(egalim_others_filter)
        externalities_performance_purchases = purchases_no_other.filter(externalities_performance_filter).distinct()
        data["value_externality_performance_ht"] = externalities_performance_purchases.aggregate(
            total=Sum("price_ht")
        )["total"]

    def _complete_diag_data(purchases, data):
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
            for label in CanteenPurchasesSummaryView.egalim_labels:
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
                data[key] = fam_label.aggregate(total=Sum("price_ht"))["total"]
            # outside of EGAlim, products can be counted twice across characteristics
            purchase_family = purchases.filter(family=family)
            other_labels_characteristics = []
            for label in other_labels:
                characteristic = Purchase.Characteristic[label]
                fam_label = purchase_family.filter(Q(characteristics__contains=[characteristic]))
                key = "value_" + family.lower() + "_" + label.lower()
                data[key] = fam_label.aggregate(total=Sum("price_ht"))["total"]
                other_labels_characteristics.append(characteristic)
            # Non-EGAlim totals: contains no labels or only one or more of other_labels
            non_egalim_purchases = purchase_family.filter(
                Q(characteristics__contained_by=other_labels_characteristics) | Q(characteristics__len=0)
            ).distinct()
            key = "value_" + family.lower() + "_non_egalim"
            data[key] = non_egalim_purchases.aggregate(total=Sum("price_ht"))["total"]

    def _misc_totals(purchases, data):
        meat_poultry_purchases = purchases.filter(
            family=Purchase.Family.VIANDES_VOLAILLES,
        )
        data["value_meat_poultry_ht"] = meat_poultry_purchases.aggregate(total=Sum("price_ht"))["total"]

        meat_poultry_egalim = meat_poultry_purchases.filter(
            characteristics__overlap=CanteenPurchasesSummaryView.egalim_labels
        )
        data["value_meat_poultry_egalim_ht"] = meat_poultry_egalim.aggregate(total=Sum("price_ht"))["total"]

        meat_poultry_france = meat_poultry_purchases.filter(
            characteristics__contains=[
                "FRANCE",
            ]
        )
        data["value_meat_poultry_france_ht"] = meat_poultry_france.aggregate(total=Sum("price_ht"))["total"]

        fish_purchases = purchases.filter(
            family=Purchase.Family.PRODUITS_DE_LA_MER,
        )
        data["value_fish_ht"] = fish_purchases.aggregate(total=Sum("price_ht"))["total"]

        fish_egalim = fish_purchases.filter(characteristics__overlap=CanteenPurchasesSummaryView.egalim_labels)
        data["value_fish_egalim_ht"] = fish_egalim.aggregate(total=Sum("price_ht"))["total"]


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


class ImportPurchasesView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        self.purchases_created = 0
        super().__init__(**kwargs)

    def post(self, request):
        start = time.time()
        logger.info("Purchase bulk import started")
        try:
            with transaction.atomic():
                file = request.data["file"]
                ImportPurchasesView._verify_file_size(file)
                (purchases, errors) = self._treat_csv_file(file)

                if errors:
                    raise IntegrityError()

            return ImportPurchasesView._get_success_response([], self.purchases_created, errors, start)

        except IntegrityError as e:
            logger.warning(f"L'import du fichier CSV a échoué:\n{e}")
            return ImportPurchasesView._get_success_response([], 0, errors, start)

        except ValidationError as e:
            message = e.message
            logger.warning(message)
            message = message
            errors = [{"row": 0, "status": 400, "message": message}]
            return ImportPurchasesView._get_success_response([], 0, errors, start)

        except Exception as e:
            message = "Échec lors de la lecture du fichier"
            logger.exception(f"{message}:\n{e}")
            errors = [{"row": 0, "status": 400, "message": message}]
            return ImportPurchasesView._get_success_response([], 0, errors, start)

    @staticmethod
    def _verify_file_size(file):
        if file.size > settings.CSV_IMPORT_MAX_SIZE:
            raise ValidationError("Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo")

    def _treat_csv_file(self, file):
        purchases = []
        errors = []

        filestring = file.read().decode("utf-8-sig")
        filelines = filestring.splitlines()
        dialect = csv.Sniffer().sniff(filelines[0])

        csvreader = csv.reader(filelines, dialect=dialect)
        for row_number, row in enumerate(csvreader, start=1):
            if row_number == 1 and row[0].lower().__contains__("siret"):
                continue
            try:
                # first check that the number of columns is good
                #   to throw error if badly formatted early on.
                if len(row) < 7:
                    raise BadRequest()
                siret = row.pop(0)
                if siret == "":
                    raise ValidationError({"siret": "Le siret de la cantine ne peut pas être vide"})
                siret = normalise_siret(siret)
                purchase = self._create_purchase_for_canteen(siret, row)
                purchases.append(purchase)

            except Exception as e:
                for error in self._parse_errors(e, row):
                    errors.append(ImportPurchasesView._get_error(e, error["message"], error["code"], row_number))
        return (purchases, errors)

    @transaction.atomic
    def _create_purchase_for_canteen(self, siret, row):
        if not Canteen.objects.filter(siret=siret).exists():
            raise ObjectDoesNotExist()
        canteen = Canteen.objects.get(siret=siret)
        if self.request.user not in canteen.managers.all():
            raise PermissionDenied(detail="Vous n'êtes pas un gestionnaire de cette cantine.")

        description = row.pop(0)
        if description == "":
            raise ValidationError({"description": "La description ne peut pas être vide"})
        provider = row.pop(0)
        if provider == "":
            raise ValidationError({"provider": "Le fournisseur ne peut pas être vide"})
        date = row.pop(0)
        if date == "":
            raise ValidationError({"date": "La date ne peut pas être vide"})
        price = row.pop(0)
        if price == "":
            raise ValidationError({"price_ht": "Le prix ne peut pas être vide"})
        family = row.pop(0)
        characteristics = row.pop(0)
        characteristics = [c.strip() for c in characteristics.split(",")]
        local_definition = row.pop(0)
        if "LOCAL" in characteristics and not local_definition:
            raise ValidationError(
                {"local_definition": "La définition de local est obligatoire pour les produits locaux"}
            )

        purchase = Purchase(
            canteen=canteen,
            description=description.strip(),
            provider=provider.strip(),
            date=date.strip(),
            price_ht=price.strip(),
            family=family.strip(),
            characteristics=characteristics,
            local_definition=local_definition.strip(),
            import_source="Import du fichier CSV",
        )
        purchase.full_clean()
        purchase.save()
        self.purchases_created += 1

        return purchase

    @staticmethod
    def _get_success_response(purchases, count, errors, start_time):
        return JsonResponse(
            {
                "purchases": purchases,
                "count": count,
                "errors": errors,
                "seconds": time.time() - start_time,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _get_verbose_field_name(field_name):
        try:
            return Purchase._meta.get_field(field_name).verbose_name
        except Exception:
            return field_name

    @staticmethod
    def _get_error(e, message, error_status, row_number):
        logger.warning(f"Error on row {row_number}:\n{e}")
        return {"row": row_number, "status": error_status, "message": message}

    def _parse_errors(self, e, row):
        errors = []
        if isinstance(e, PermissionDenied):
            errors.append(
                {
                    "message": e.detail,
                    "code": 401,
                }
            )
        elif isinstance(e, BadRequest):
            errors.append(
                {
                    "message": f"Format fichier : 7-8 colonnes attendues, {len(row)} trouvées.",
                    "code": 400,
                }
            )
        elif isinstance(e, ObjectDoesNotExist):
            errors.append(
                {
                    "message": "Cantine non trouvée.",
                    "code": 404,
                }
            )
        elif isinstance(e, ValidationError):
            if e.message_dict:
                for field, messages in e.message_dict.items():
                    verbose_field_name = ImportPurchasesView._get_verbose_field_name(field)
                    for message in messages:
                        user_message = message
                        if field != "__all__":
                            user_message = f"Champ '{verbose_field_name}' : {user_message}"
                        errors.append(
                            {
                                "message": user_message,
                                "code": 400,
                            }
                        )
        if not errors:
            errors.append(
                {
                    "message": "Une erreur s'est produite en créant un achat pour cette ligne",
                    "code": 400,
                }
            )
        return errors
