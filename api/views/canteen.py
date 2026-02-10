import logging
from collections import OrderedDict
from datetime import date

import redis as r
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest, ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.db.models import FloatField, Q, Sum
from django.db.models.functions import Cast
from drf_excel.mixins import XLSXFileMixin
from drf_excel.renderers import XLSXRenderer
from django.http import JsonResponse
from django_filters import BaseInFilter, CharFilter
from django_filters import rest_framework as django_filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, MethodNotAllowed
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.exceptions import DuplicateException
from api.filters.utils import MaCantineOrderingFilter, UnaccentSearchFilter
from api.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrTokenHasResourceScope,
    IsCanteenManager,
    IsElectedOfficial,
)
from api.serializers import (
    CanteenActionsLightSerializer,
    CanteenActionsSerializer,
    CanteenAnalysisSerializer,
    CanteenMinistriesSerializer,
    CanteenOpenDataSerializer,
    CanteenPreviewSerializer,
    CanteenStatusSerializer,
    CanteenSummarySerializer,
    ElectedCanteenSerializer,
    FullCanteenSerializer,
    ManagingTeamSerializer,
    CanteenExportSerializer,
    MinimalCanteenSerializer,
    PublicCanteenPreviewSerializer,
    PublicCanteenSerializer,
)
from api.views.utils import update_change_reason_with_auth
from common.api.adresse import fetch_geo_data_from_code
from common.api.recherche_entreprises import fetch_geo_data_from_siren, fetch_geo_data_from_siret
from common.utils import send_mail
from data.models import Canteen, Diagnostic, ManagerInvitation, Sector, SectorM2M
from data.models.creation_source import CreationSource
from data.utils import has_charfield_missing_query

logger = logging.getLogger(__name__)
redis = r.from_url(settings.REDIS_URL, decode_responses=True)


class PublishedCanteenSingleView(RetrieveAPIView):
    model = Canteen
    serializer_class = PublicCanteenSerializer

    def get_queryset(self):
        return Canteen.objects.annotate_with_is_managed_by_user(self.request.user).publicly_visible()


class ProductionTypeInFilter(BaseInFilter, CharFilter):
    pass


class PublishedCanteensPagination(LimitOffsetPagination):
    default_limit = 12
    max_limit = 30
    departments = []
    sectors = []
    management_types = []
    production_types = []

    def paginate_queryset(self, queryset, request, view=None):
        # Performance improvements possible
        self.departments = set(filter(lambda x: x, queryset.values_list("department", flat=True)))
        self.regions = set(filter(lambda x: x, queryset.values_list("region", flat=True)))
        self.management_types = set(filter(lambda x: x, queryset.values_list("management_type", flat=True)))
        self.production_types = set(filter(lambda x: x, queryset.values_list("production_type", flat=True)))

        # Prepare sector filter options:
        # we want to return all sectors that are available after the other filters,
        # because the user can select multiple sectors (unlike other filter options)
        all_sector_canteens = Canteen.objects.publicly_visible()
        query_params = request.query_params
        if query_params.get("department"):
            all_sector_canteens = all_sector_canteens.filter(department=query_params.get("department"))
        if query_params.get("region"):
            all_sector_canteens = all_sector_canteens.filter(region=query_params.get("region"))
        if query_params.get("min_daily_meal_count"):
            all_sector_canteens = all_sector_canteens.filter(
                daily_meal_count__gte=query_params.get("min_daily_meal_count")
            )
        if query_params.get("max_daily_meal_count"):
            all_sector_canteens = all_sector_canteens.filter(
                daily_meal_count__lte=query_params.get("max_daily_meal_count")
            )
        if query_params.get("management_type"):
            all_sector_canteens = all_sector_canteens.filter(management_type=query_params.get("management_type"))
        all_sector_canteens = filter_by_diagnostic_params(all_sector_canteens, query_params)

        self.sectors = (
            SectorM2M.objects.filter(canteen__in=list(all_sector_canteens)).values_list("id", flat=True).distinct()
        )

        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                    ("regions", self.regions),
                    ("departments", self.departments),
                    ("sectors", self.sectors),
                    ("management_types", self.management_types),
                    ("production_types", self.production_types),
                ]
            )
        )


class UserCanteensPagination(LimitOffsetPagination):
    default_limit = 12
    max_limit = 30

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


class CanteenActionsPagination(LimitOffsetPagination):
    default_limit = 12
    max_limit = 30
    undiagnosed_canteens_with_purchases = []
    has_pending_actions = False

    def paginate_queryset(self, queryset, request, view=None):
        undiagnosed_canteens_with_purchases = queryset.filter(action=Canteen.Actions.PREFILL_DIAGNOSTIC).values_list(
            "pk", flat=True
        )
        self.undiagnosed_canteens_with_purchases = set(filter(lambda x: x, undiagnosed_canteens_with_purchases))
        self.has_pending_actions = queryset.exclude(action=Canteen.Actions.NOTHING).exists()
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                    ("undiagnosed_canteens_with_purchases", self.undiagnosed_canteens_with_purchases),
                    ("has_pending_actions", self.has_pending_actions),
                ]
            )
        )


class PublishedCanteenFilterSet(django_filters.FilterSet):
    min_daily_meal_count = django_filters.NumberFilter(field_name="daily_meal_count", lookup_expr="gte")
    max_daily_meal_count = django_filters.NumberFilter(field_name="daily_meal_count", lookup_expr="lte")
    production_type = ProductionTypeInFilter(field_name="production_type")
    sector = django_filters.MultipleChoiceFilter(
        field_name="sector_list", choices=Sector.choices, lookup_expr="icontains"
    )

    class Meta:
        model = Canteen
        fields = (
            "department",
            "region",
            "sector",
            "city_insee_code",
            "min_daily_meal_count",
            "max_daily_meal_count",
            "management_type",
        )


def filter_by_diagnostic_params(queryset, query_params):
    param_bio_rate = query_params.get("min_portion_bio")
    param_combined_rate = query_params.get("min_portion_combined")
    param_badge = query_params.get("badge")
    appro_badge_requested = param_badge == "appro"
    if param_bio_rate or param_combined_rate or appro_badge_requested:
        publication_year = date.today().year - 1
        qs_diag = Diagnostic.objects.filled().in_year(publication_year)
        if param_bio_rate or appro_badge_requested:
            qs_diag = qs_diag.annotate(
                bio_percent=100 * Cast(Sum("valeur_bio", default=0) / Sum("valeur_totale"), FloatField())
            )
            if param_bio_rate:
                qs_diag = qs_diag.filter(bio_percent__gte=100 * float(param_bio_rate))
        if param_combined_rate or appro_badge_requested:
            qs_diag = qs_diag.annotate(
                egalim_percent=100
                * Cast(
                    (
                        Sum("valeur_bio", default=0)
                        + Sum("valeur_siqo", default=0)
                        + Sum("valeur_externalites_performance", default=0)
                        + Sum("valeur_egalim_autres", default=0)
                    )
                    / Sum("valeur_totale"),
                    FloatField(),
                )
            )
            if param_combined_rate:
                qs_diag = qs_diag.filter(egalim_percent__gte=100 * float(param_combined_rate))
        if appro_badge_requested:
            qs_diag = qs_diag.egalim_objectives_reached().distinct()
        canteen_ids = qs_diag.values_list("canteen", flat=True)
        canteen_sirets = qs_diag.exclude(has_charfield_missing_query("canteen__siret")).values_list(
            "canteen__siret", flat=True
        )
        queryset = queryset.exclude(redacted_appro_years__contains=[publication_year])
        return queryset.filter(Q(id__in=canteen_ids) | Q(central_producer_siret__in=canteen_sirets))
    return queryset


class PublishedCanteensView(ListAPIView):
    model = Canteen
    serializer_class = PublicCanteenPreviewSerializer
    queryset = Canteen.objects.publicly_visible()
    pagination_class = PublishedCanteensPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
        UnaccentSearchFilter,
        MaCantineOrderingFilter,
    ]
    # TODO: maybe add city/region/department name?
    search_fields = ["name", "siret"]
    ordering_fields = ["name", "creation_date", "modification_date", "daily_meal_count"]
    filterset_class = PublishedCanteenFilterSet

    def filter_queryset(self, queryset):
        new_queryset = filter_by_diagnostic_params(queryset, self.request.query_params)
        return super().filter_queryset(new_queryset)


class PublicCanteenPreviewView(RetrieveAPIView):
    model = Canteen
    serializer_class = PublicCanteenPreviewSerializer
    queryset = Canteen.objects.publicly_visible()


class UserCanteensFilterSet(django_filters.FilterSet):
    production_type = ProductionTypeInFilter(field_name="production_type")


@extend_schema_view(
    get=extend_schema(
        summary="Lister avec une pagination des cantines gérées par l'utilisateur. Représentation complète.",
        description="Une pagination est mise en place pour cet endpoint. La représentation de la cantine est complète.",
    ),
    post=extend_schema(
        summary="Créer une nouvelle cantine.",
        description="La nouvelle cantine aura comme gestionnaire l'utilisateur identifié.",
    ),
)
class UserCanteensView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope]
    model = Canteen
    serializer_class = FullCanteenSerializer
    pagination_class = UserCanteensPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
        UnaccentSearchFilter,
        MaCantineOrderingFilter,
    ]
    filterset_class = UserCanteensFilterSet
    required_scopes = ["canteen"]
    search_fields = ["name", "siret"]
    ordering_fields = ["name", "creation_date", "modification_date", "daily_meal_count"]

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault("context", self.get_serializer_context())
        action = "create" if self.request.method == "POST" else None
        kwargs.setdefault("action", action)
        return FullCanteenSerializer(*args, **kwargs)

    def get_queryset(self):
        return self.request.user.canteens.all()

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        creation_source = serializer.validated_data.get("creation_source") or CreationSource.API
        canteen = serializer.save(creation_source=creation_source)
        canteen.managers.add(self.request.user)
        update_change_reason_with_auth(self, canteen)

    def create(self, request, *args, **kwargs):
        """
        Custom API checks
        - duplicate SIRET are not allowed
        - users cannot create CENTRAL or CENTRAL_SERVING canteens  # TODO: move to validators/canteen.py
        """
        canteen_siret = request.data.get("siret")
        error_response = get_cantine_from_siret(canteen_siret, request)
        if error_response:
            raise DuplicateException(additional_data=error_response)
        production_type = request.data.get("production_type")
        if production_type in [
            Canteen.ProductionType.CENTRAL,
            Canteen.ProductionType.CENTRAL_SERVING,
        ]:
            return JsonResponse(
                {
                    "production_type": [
                        "La création de cantines de type CENTRAL ou CENTRAL_SERVING n'est plus autorisée."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(
        summary="Lister toutes les cantines gérées par l'utilisateur. Représentation partielle.",
        description="La totalité des cantines gérées par l'utilisateur - par contre seules certaines informations sont incluses.",
    ),
)
class UserCanteenPreviews(ListAPIView):
    model = Canteen
    serializer_class = CanteenPreviewSerializer
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope]
    required_scopes = ["canteen"]

    def get_queryset(self):
        return self.request.user.canteens.all()


class UserCanteenSummaries(ListAPIView):
    model = Canteen
    serializer_class = CanteenSummarySerializer
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope]
    required_scopes = ["canteen"]
    pagination_class = UserCanteensPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
        UnaccentSearchFilter,
        MaCantineOrderingFilter,
    ]
    filterset_class = UserCanteensFilterSet
    search_fields = ["name", "siret"]
    ordering_fields = ["name", "creation_date", "modification_date", "daily_meal_count"]

    def get_queryset(self):
        return self.request.user.canteens.all()


class UserCanteenActions(ListAPIView):
    permission_classes = [IsAuthenticated]
    model = Canteen
    serializer_class = CanteenActionsLightSerializer

    def get_queryset(self):
        year = self.request.parser_context.get("kwargs").get("year")
        user_canteen_queryset = self.request.user.canteens.order_by("name")
        return user_canteen_queryset.select_related("groupe").annotate_with_action_for_year(year)


class UserCanteenListExportView(UserCanteenActions, XLSXFileMixin):
    renderer_classes = (XLSXRenderer,)
    pagination_class = None
    serializer_class = CanteenExportSerializer

    # same as data/schemas/imports/cantines.json
    column_header = {
        "titles": [
            "siret",
            "nom",
            "siret_cuisine_centrale",
            "nombre_repas_jour",
            "nombre_repas_an",
            "secteurs",
            "type_production",
            "type_gestion",
            "modèle_économique",
            "groupe_id",
            "administration_tutelle",
            "gestionnaires",
        ],
        # "column_width": [],
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


@extend_schema_view(
    get=extend_schema(
        summary="Obtenir les détails d'une cantine.",
        description="Permet d'obtenir toutes les informations sur une cantine spécifique tant que l'utilisateur soit un des gestionnaires.",
    ),
    put=extend_schema(
        exclude=True,
    ),
    patch=extend_schema(
        summary="Modifier une cantine existante.",
        description="Possible si l'utilisateur identifié fait partie des gestionnaires de la cantine.",
    ),
    delete=extend_schema(
        summary="Supprimer une cantine existante.",
        description="Possible si l'utilisateur identifié fait partie des gestionnaires de la cantine. Attention : les diagnostics créés seront aussi supprimés.",
    ),
)
class RetrieveUpdateUserCanteenView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManager]
    model = Canteen
    serializer_class = FullCanteenSerializer
    queryset = Canteen.objects.all()
    required_scopes = ["canteen"]

    def put(self, request, *args, **kwargs):
        return JsonResponse(
            {"error": "Only PATCH request supported in this resource"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        canteen_siret = request.data.get("siret")
        if "siret" in request.data and not canteen_siret:
            return JsonResponse(
                {"siret": ["Le numéro SIRET ne peut pas être vide."]}, status=status.HTTP_400_BAD_REQUEST
            )
        error_response = get_cantine_from_siret(canteen_siret, request)
        if error_response and error_response.get("id") != kwargs.get("pk"):
            raise DuplicateException(additional_data=error_response)
        return super().partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        canteen = serializer.save()
        update_change_reason_with_auth(self, canteen)

    def perform_destroy(self, instance):
        instance.delete(skip_validations=True)


class CanteenStatusBySiretView(APIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope]
    required_scopes = ["canteen"]

    def get(self, request, *args, **kwargs):
        siret = request.parser_context.get("kwargs").get("siret")
        response = get_cantine_from_siret(siret, request) or {}
        if not response:
            response = fetch_geo_data_from_siret(siret)
            if not response:
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            city = response.get("city", None)
            postcode = response.get("postalCode", None)
            if city and postcode:
                response = fetch_geo_data_from_code(response)
        return Response(response, status=status.HTTP_200_OK)


class CanteenStatusBySirenView(APIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope]
    required_scopes = ["canteen"]

    def get(self, request, *args, **kwargs):
        siren = request.parser_context.get("kwargs").get("siren")
        response = fetch_geo_data_from_siren(siren)
        if not response:
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        response["canteens"] = get_cantine_list_from_siren_unite_legale(siren, request)
        return Response(response, status=status.HTTP_200_OK)


def get_cantine_from_siret(siret, request):
    if siret:
        canteens = Canteen.objects.annotate_with_is_managed_by_user(request.user).filter(siret=siret)
        if canteens.exists():
            canteen = canteens.first()
            return CanteenStatusSerializer(canteen, context={"request": request}).data


def get_cantine_list_from_siren_unite_legale(siren, request):
    if siren:
        canteens = (
            Canteen.objects.annotate_with_is_managed_by_user(request.user)
            .filter(siren_unite_legale=siren)
            .order_by("name")
        )
        return CanteenStatusSerializer(canteens, many=True, context={"request": request}).data


class AddManagerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email").strip() if request.data.get("email") else None
            validate_email(email)
            canteen_id = request.data.get("canteen_id")
            canteen = request.user.canteens.get(id=canteen_id)
            AddManagerView.add_manager_to_canteen(email, canteen)
            return Response(ManagingTeamSerializer(canteen).data, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.warning(f"Attempt to add manager with invalid email {email}:\n{e}")
            return JsonResponse({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        except Canteen.DoesNotExist as e:
            logger.warning(f"Attempt to add manager to unexistent canteen {canteen_id}:\n{e}")
            return JsonResponse({"error": "Invalid canteen id"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            logger.warning(f"Attempt to add existing manager with email {email} to canteen {canteen_id}:\n{e}")
            return Response(ManagingTeamSerializer(canteen).data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(f"Exception occurred while inviting a manager to canteen:\n{e}")
            return JsonResponse(
                {"error": "An error has occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def add_manager_to_canteen(email, canteen, send_invitation_mail=True):
        try:
            user = get_user_model().objects.get(email=email)
            canteen.managers.add(user)
            if send_invitation_mail:
                AddManagerView._send_add_email(email, canteen)
        except get_user_model().DoesNotExist:
            # Try to see if the user registered the email with case irregularities
            user_qs = get_user_model().objects.filter(email__iexact=email)
            if user_qs.count() == 1:
                user = user_qs.first()
                logger.info(f"Adding manager with email in different case : {email}")
                canteen.managers.add(user)
                if send_invitation_mail:
                    AddManagerView._send_add_email(user.email, canteen)
                return

            if user_qs.count() > 1:
                logger.info(f"Several users found for the case-insensitive email {email}. Unable to add manager.")

            with transaction.atomic():
                pm = ManagerInvitation(canteen_id=canteen.id, email=email)
                pm.save()
            if send_invitation_mail:
                AddManagerView._send_invitation_email(pm)

    @staticmethod
    def _send_invitation_email(manager_invitation):
        try:
            context = {
                "canteen": manager_invitation.canteen.name,
                "protocol": settings.PROTOCOL,
                "domain": settings.HOSTNAME,
            }
            send_mail(
                subject="Invitation à gérer une cantine sur ma cantine",
                template="auth/manager_invitation",
                context=context,
                to=[manager_invitation.email],
            )
        except ConnectionRefusedError as e:
            logger.warning(
                f"The manager invitation email could not be sent to {manager_invitation.email} : Connection Refused. The manager has been added anyway.\n{e}"
            )
            return
        except Exception as e:
            logger.exception(f"The manager invitation email could not be sent to {manager_invitation.email}\n{e}")
            raise Exception("Error occurred : the mail could not be sent.") from e

    @staticmethod
    def _send_add_email(email, canteen):
        try:
            protocol = settings.PROTOCOL
            domain = settings.HOSTNAME
            canteen_path = f"/modifier-ma-cantine/{canteen.url_slug}"
            context = {
                "canteen": canteen.name,
                "canteen_url": f"{protocol}://{domain}{canteen_path}",
            }
            send_mail(
                subject=f"Vous pouvez gérer la cantine « {canteen.name} »",
                template="auth/manager_add_notification",
                context=context,
                to=[email],
            )
        except ConnectionRefusedError as e:
            logger.warning(
                f"The manager add notification email could not be sent to {email} : Connection Refused. The manager has been added anyway.\n{e}"
            )
            return
        except Exception as e:
            logger.exception(f"The manager add notification email could not be sent to {email}\n{e}")
            raise Exception("Error occurred : the mail could not be sent.") from e


class RemoveManagerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email", "").strip()
            validate_email(email)
            canteen_id = request.data.get("canteen_id")
            canteen = request.user.canteens.get(id=canteen_id)

            try:
                manager = get_user_model().objects.get(email=email)
                canteen.managers.remove(manager)
            except get_user_model().DoesNotExist:
                try:
                    invitation = ManagerInvitation.objects.get(canteen_id=canteen.id, email=email)
                    invitation.delete()
                except ManagerInvitation.DoesNotExist:
                    pass
            return Response(ManagingTeamSerializer(canteen).data, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.warning(f"Attempt to remove manager with invalid email {email}:\n{e}")
            return JsonResponse({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        except Canteen.DoesNotExist as e:
            logger.warning(f"Attempt to remove manager from unexistent canteen {canteen_id}:\n{e}")
            return JsonResponse({"error": "Invalid canteen id"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(f"Exception occurred while removing a manager from a canteen:\n{e}")
            return JsonResponse(
                {"error": "An error has occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SendCanteenNotFoundEmail(APIView):
    def post(self, request):
        try:
            email = request.data.get("from", "").strip()
            validate_email(email)
            name = request.data.get("name") or "Un·e utilisateur·rice"
            message = request.data.get("message")

            context = {
                "from": email,
                "name": name,
                "message": message,
            }

            send_mail(
                subject=f"{name} n'a pas trouvé une cantine publiée",
                to=[
                    settings.CONTACT_EMAIL,
                ],
                reply_to=[
                    email,
                ],
                template="canteen_not_found",
                context=context,
            )

            return JsonResponse({}, status=status.HTTP_200_OK)
        except ValidationError:
            return JsonResponse({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"Exception occurred while sending email:\n{e}")
            return JsonResponse(
                {"error": "An error has occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TeamJoinRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email", "").strip()
            validate_email(email)
            name = request.data.get("name")
            message = request.data.get("message")
            canteen_id = kwargs.get("pk")
            canteen = Canteen.objects.get(pk=canteen_id)
            canteen_path = f"/modifier-ma-cantine/{canteen.url_slug}"
            url = f"{'https' if settings.SECURE else 'http'}://{settings.HOSTNAME}{canteen_path}/gestionnaires?email={email}"

            context = {
                "email": email,
                "name": name,
                "message": message,
                "url": url,
                "canteen": canteen.name,
                "siret": canteen.siret,
                "siren_unite_legale": canteen.siren_unite_legale,
            }

            recipients = list(canteen.managers.values_list("email", flat=True))

            if not recipients:
                recipients.append(settings.CONTACT_EMAIL)

            send_mail(
                subject=f"{name} voudrait rejoindre l'équipe de gestion de la cantine {canteen.name}",
                to=recipients,
                reply_to=[email],
                template="canteen_join_request",
                context=context,
            )

            return JsonResponse({}, status=status.HTTP_200_OK)
        except ValidationError:
            return JsonResponse({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"Exception occurred while sending email:\n{e}")
            return JsonResponse(
                {"error": "An error has occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ClaimCanteenView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, canteen_pk):
        try:
            canteen = Canteen.objects.get(pk=canteen_pk)
        except Canteen.DoesNotExist:
            raise BadRequest()

        if canteen.managers.exists():
            raise BadRequest()

        canteen.managers.add(self.request.user)
        canteen.claimed_by = self.request.user
        canteen.has_been_claimed = True
        canteen.save()
        return Response(MinimalCanteenSerializer(canteen).data, status=status.HTTP_200_OK)


class UndoClaimCanteenView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, canteen_pk):
        try:
            canteen = Canteen.objects.get(pk=canteen_pk)
        except Canteen.DoesNotExist:
            raise BadRequest()

        if canteen.claimed_by != self.request.user:
            raise PermissionDenied()

        canteen.managers.remove(self.request.user)
        canteen.claimed_by = None
        canteen.has_been_claimed = False
        canteen.save()
        return JsonResponse({}, status=status.HTTP_200_OK)


class ActionableCanteensListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    model = Canteen
    serializer_class = CanteenActionsSerializer
    pagination_class = CanteenActionsPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
        UnaccentSearchFilter,
        MaCantineOrderingFilter,
    ]
    search_fields = ["name", "siret", "siren_unite_legale"]
    ordering_fields = ["name", "production_type", "action", "modification_date"]
    ordering = "modification_date"

    def get_queryset(self):
        year = self.request.parser_context.get("kwargs").get("year")
        user_canteen_queryset = self.request.user.canteens
        return user_canteen_queryset.annotate_with_action_for_year(year)


class ActionableCanteenRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsCanteenManager]
    model = Canteen
    serializer_class = CanteenActionsSerializer
    required_scopes = ["canteen"]

    def get_queryset(self):
        year = self.request.parser_context.get("kwargs").get("year")
        canteen_id = self.request.parser_context.get("kwargs").get("pk")
        single_canteen_queryset = self.request.user.canteens.filter(id=canteen_id)
        return single_canteen_queryset.annotate_with_action_for_year(year)


class TerritoryCanteensListView(ListAPIView):
    model = Canteen
    permission_classes = [IsElectedOfficial]
    serializer_class = ElectedCanteenSerializer
    pagination_class = PublishedCanteensPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
        UnaccentSearchFilter,
        MaCantineOrderingFilter,
    ]
    search_fields = ["name", "siret"]
    ordering_fields = ["name", "city", "siret", "daily_meal_count"]

    def get_queryset(self):
        departments = self.request.user.departments
        return Canteen.objects.annotate_with_is_managed_by_user(self.request.user).filter(department__in=departments)


@extend_schema_view(
    get=extend_schema(
        summary="Lister les options pour le ministère de tutelle.",
        description="Certains secteurs nécessite la spécification d'un ministère du tutelle.",
    ),
)
class CanteenMinistriesView(APIView):
    include_in_documentation = True
    required_scopes = ["canteen"]

    @extend_schema(responses=CanteenMinistriesSerializer(many=True))
    def get(self, request, format=None):
        ministries = []
        for ministry in Canteen.Ministries:
            ministries.append(
                {
                    "value": ministry.value,
                    "name": ministry.label,
                }
            )
        return Response(CanteenMinistriesSerializer(ministries, many=True).data)


class CanteenAnalysisListView(ListAPIView):
    serializer_class = CanteenAnalysisSerializer

    def get_queryset(self):
        return Canteen.objects.prefetch_related("sectors_m2m", "managers").order_by("creation_date")


class CanteenOpenDataListView(ListAPIView):
    serializer_class = CanteenOpenDataSerializer

    def get_queryset(self):
        return Canteen.objects.prefetch_related("sectors_m2m", "managers").publicly_visible().order_by("creation_date")
