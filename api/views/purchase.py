import logging
from collections import OrderedDict

from django.core.exceptions import BadRequest, ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from django_filters import rest_framework as django_filters
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters.utils import UnaccentSearchFilter
from api.permissions import (
    IsAuthenticated,
    IsCanteenManager,
    IsAuthenticatedOrTokenHasResourceScope,
    IsCanteenManagerUrlParam,
    IsLinkedCanteenManager,
)
from api.serializers import (
    PurchaseFactureResponseSerializer,
    PurchaseFactureUploadSerializer,
    PurchaseOldSerializer,
    PurchasePercentageSummarySerializer,
    PurchaseSerializer,
    PurchaseSummarySerializer,
)
from api.views.utils import get_oauth_application
from data.models import Canteen, Diagnostic, Purchase
from data.models.creation_source import CreationSource

logger = logging.getLogger(__name__)


class PurchaseCreateView(CreateModelMixin, GenericAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    http_method_names = ["post"]
    model = Purchase
    serializer_class = PurchaseSerializer

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def perform_create(self, serializer):
        canteen = self._get_canteen()
        serializer.is_valid(raise_exception=True)
        creation_user = self.request.user
        creation_source = serializer.validated_data.get("creation_source") or CreationSource.API
        creation_source_api_oauth2_application = get_oauth_application(self.request)
        serializer.save(
            canteen=canteen,
            creation_user=creation_user,
            creation_source=creation_source,
            creation_source_api_oauth2_application=creation_source_api_oauth2_application,
        )

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PurchaseRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    http_method_names = ["get", "patch", "delete"]  # disable "put"
    model = Purchase
    serializer_class = PurchaseSerializer

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def get_queryset(self):
        canteen = self._get_canteen()
        return Purchase.objects.filter(canteen=canteen)


class PurchasesPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 500
    families = []
    characteristics = []
    canteens = []

    def paginate_queryset(self, queryset, request, view=None):
        """
        return extra fields for the filter options in the frontend
        - queryset's list of values for famille_produits, caracteristiques and canteens
        - and not only for the current page
        """
        self.families = list(set(queryset.values_list("famille_produits", flat=True)))
        self.characteristics = list(
            {
                characteristic
                for characteristics in queryset.values_list("caracteristiques", flat=True)
                for characteristic in characteristics
            }
        )
        self.canteen_ids = list(set(queryset.values_list("canteen__id", flat=True)))

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
                    ("canteens", self.canteen_ids),
                ]
            )
        )


class PurchaseFilterSet(django_filters.FilterSet):
    # TODO: move to Meta.fields once we finish the translation to French
    family = django_filters.CharFilter(field_name="famille_produits")
    characteristics = django_filters.CharFilter(method="filter_caracteristiques")
    date = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Purchase
        fields = (
            "canteen__id",
            # "family",
            # "characteristics",
            # "date"
        )

    # caracteristiques is a ChoiceArrayField, we need a custom overlap filter
    def filter_caracteristiques(self, queryset, name, value):
        caracteristiques = self.request.query_params.getlist("characteristics")
        if caracteristiques:
            return queryset.filter(caracteristiques__overlap=caracteristiques)
        return queryset


class PurchaseOldListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsLinkedCanteenManager]
    model = Purchase
    serializer_class = PurchaseOldSerializer
    pagination_class = PurchasesPagination
    filter_backends = [
        UnaccentSearchFilter,
        django_filters.DjangoFilterBackend,
    ]
    ordering_fields = [
        "creation_date",
        "date",
        "fournisseur",
        "prix_ht",
        "canteen__name",
        "description",
        "famille_produits",
    ]
    search_fields = [
        "description",
        "fournisseur",
    ]
    filterset_class = PurchaseFilterSet

    def get_queryset(self):
        return Purchase.objects.for_user(self.request.user)

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
            creation_user = self.request.user
            creation_source = serializer.validated_data.get("creation_source") or CreationSource.API
            creation_source_api_oauth2_application = get_oauth_application(self.request)
            serializer.save(
                canteen=canteen,
                creation_user=creation_user,
                creation_source=creation_source,
                creation_source_api_oauth2_application=creation_source_api_oauth2_application,
            )
        except ObjectDoesNotExist as e:
            logger.error(
                f"User {self.request.user.id} attempted to create a purchase in nonexistent canteen {canteen_id}"
            )
            raise NotFound() from e


class PurchaseOldRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsLinkedCanteenManager]
    http_method_names = ["get", "patch", "delete"]  # disable "put"
    model = Purchase
    serializer_class = PurchaseOldSerializer

    def get_queryset(self):
        return Purchase.objects.for_user(self.request.user)

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


class PurchaseFactureView(APIView):
    permission_classes = [IsAuthenticated, IsCanteenManagerUrlParam]
    http_method_names = ["get", "post", "delete"]

    def get_object(self):
        return get_object_or_404(Purchase, pk=self.kwargs.get("pk"), canteen__pk=self.kwargs.get("canteen_pk"))

    def get(self, request, *args, **kwargs):
        purchase = self.get_object()

        if not purchase.facture:
            raise NotFound()

        serializer = PurchaseFactureResponseSerializer(purchase, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        purchase = self.get_object()

        serializer = PurchaseFactureUploadSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        purchase.facture = serializer.validated_data["facture"]
        purchase.save()

        response_serializer = PurchaseFactureResponseSerializer(purchase, context={"request": request})
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        purchase = self.get_object()

        if not purchase.facture:
            raise NotFound()

        purchase.facture.delete()
        purchase.facture = None
        purchase.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CanteenPurchasesSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        canteen_id = kwargs.get("canteen_pk")
        canteen = self._get_canteen(canteen_id, self.request)
        year = request.query_params.get("year")
        data = Purchase.canteen_summary_for_year(canteen, year) if year else Purchase.canteen_summary(canteen)
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

        data = Purchase.canteen_percentage_summary_for_year(canteen, year)

        if data["valeur_totale"] == 0:
            raise NotFound()

        if is_canteen_manager:
            data["last_purchase_date"] = (
                Purchase.objects.only("date").filter(canteen=canteen).for_year(year).latest("date").date
            )

        return Response(PurchasePercentageSummarySerializer(data).data)

    def _get_canteen(self, canteen_id, request):
        try:
            canteen = Canteen.objects.get(pk=canteen_id)
            return canteen
        except Canteen.DoesNotExist as e:
            raise NotFound() from e


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
            values_dict = Purchase.canteen_summary_for_year(canteen, year)
            valeur_totale = values_dict["valeur_totale"]
            if valeur_totale == 0 or valeur_totale is None:
                errors.append(f"Aucun achat trouvé pour la cantine : {canteen_id}")
                continue
            if canteen.is_groupe:
                values_dict["central_kitchen_diagnostic_mode"] = Diagnostic.CentralKitchenDiagnosticMode.APPRO
            diagnostic = Diagnostic(canteen=canteen, diagnostic_type=Diagnostic.DiagnosticType.COMPLETE, **values_dict)
            try:
                diagnostic.full_clean()
                diagnostic.save()
                created_diags.append(diagnostic.id)
            except ValidationError:
                errors.append(f"Il existe déjà un diagnostic pour l'année {year} pour la cantine : {canteen_id}")
                continue
        return JsonResponse({"results": created_diags, "errors": errors}, status=status.HTTP_201_CREATED)


class PurchaseOptionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        purchases = Purchase.objects.for_user(request.user)
        products = list(
            purchases.filter(description__isnull=False)
            .order_by("description")
            .distinct("description")
            .values_list("description", flat=True)
        )
        providers = list(
            purchases.filter(fournisseur__isnull=False)
            .order_by("fournisseur")
            .distinct("fournisseur")
            .values_list("fournisseur", flat=True)
        )
        return JsonResponse({"products": products, "providers": providers}, status=200)


class PurchasesDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        purchase_ids = request.data.get("ids")
        purchases = Purchase.objects.for_user(request.user).filter(id__in=purchase_ids)
        deleted_count = purchases.delete()
        return JsonResponse({"count": deleted_count}, status=status.HTTP_200_OK)


class PurchasesRestoreView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        purchase_ids = request.data.get("ids")
        purchases_to_restore = Purchase.all_objects.for_user(request.user).filter(id__in=purchase_ids)
        restored_count = purchases_to_restore.update(deletion_date=None)
        return JsonResponse({"count": restored_count}, status=status.HTTP_200_OK)
