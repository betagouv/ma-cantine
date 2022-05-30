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
from django.db.models import Sum, Q, Func, F
from django.http import JsonResponse
from django_filters import rest_framework as django_filters
from api.permissions import IsLinkedCanteenManager, IsCanteenManager, IsAuthenticated
from api.serializers import PurchaseSerializer, PurchaseSummarySerializer, PurchaseExportSerializer
from data.models import Purchase, Canteen
from .utils import CamelCaseOrderingFilter, UnaccentSearchFilter, normalise_siret
from collections import OrderedDict
import logging
import csv
import time


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

            # serialized_purchases = [camelize(PurchaseExportSerializer(purchase).data) for purchase in purchases]
            return ImportPurchasesView._get_success_response([], self.purchases_created, errors, start)

        except IntegrityError as e:
            logger.exception(e)
            logger.error("L'import du fichier CSV a échoué")
            return ImportPurchasesView._get_success_response([], 0, errors, start)

        except ValidationError as e:
            message = e.message
            logger.error(message)
            message = message
            errors = [{"row": 0, "status": 400, "message": message}]
            return ImportPurchasesView._get_success_response([], 0, errors, start)

        except Exception as e:
            logger.exception(e)
            message = "Échec lors de la lecture du fichier"
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
                #   NB: popped siret before this so columns are 1 less
                if len(row) < 7:
                    # TODO: why permission denied ?
                    raise PermissionDenied(detail=f"Format fichier : 7-8 colonnes attendues, {len(row)} trouvés.")
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
        category = row.pop(0)
        characteristics = row.pop(0)
        characteristics = characteristics.split(",")
        local_definition = row.pop(0)
        if "LOCAL" in characteristics and not local_definition:
            raise ValidationError(
                {"local_definition": "La définition de local est obligatoire pour les produits locaux"}
            )

        purchase = Purchase(
            canteen=canteen,
            description=description,
            provider=provider,
            date=date,
            price_ht=price,
            category=category,
            characteristics=characteristics,
            local_definition=local_definition,
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
        logger.error(f"Error on row {row_number}")
        logger.exception(e)
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
                    "message": "Une erreur s'est produite en créant un diagnostic pour cette ligne",
                    "code": 400,
                }
            )
        return errors
