import logging
from collections import OrderedDict
from datetime import date

import redis as r
import requests
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest, ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.db.models import (
    Avg,
    Case,
    Count,
    Exists,
    F,
    FloatField,
    Func,
    OuterRef,
    Q,
    Subquery,
    Sum,
    Value,
    When,
)
from django.db.models.functions import Cast
from django.http import JsonResponse
from django_filters import BaseInFilter, CharFilter
from django_filters import rest_framework as django_filters
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.exceptions import DuplicateException
from api.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrTokenHasResourceScope,
    IsCanteenManager,
    IsCanteenManagerUrlParam,
    IsElectedOfficial,
)
from api.serializers import (
    CanteenActionsSerializer,
    CanteenPreviewSerializer,
    CanteenStatusSerializer,
    CanteenSummarySerializer,
    ElectedCanteenSerializer,
    FullCanteenSerializer,
    ManagingTeamSerializer,
    MinimalCanteenSerializer,
    PublicCanteenPreviewSerializer,
    PublicCanteenSerializer,
    SatelliteCanteenSerializer,
)
from api.views.utils import update_change_reason_with_auth
from common.utils import get_token_sirene, send_mail
from data.department_choices import Department
from data.models import (
    Canteen,
    Diagnostic,
    ManagerInvitation,
    Purchase,
    Sector,
    Teledeclaration,
)
from data.region_choices import Region
from macantine.utils import (
    fetch_geo_data_from_api_entreprise_by_siret,
    fetch_geo_data_from_api_insee_sirene_by_siret,
)

from .utils import MaCantineOrderingFilter, UnaccentSearchFilter, camelize

logger = logging.getLogger(__name__)
redis = r.from_url(settings.REDIS_URL, decode_responses=True)


class PublishedCanteenSingleView(RetrieveAPIView):
    model = Canteen
    serializer_class = PublicCanteenSerializer

    def get_queryset(self):
        return Canteen.objects.publicly_visible()


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
            Sector.objects.filter(canteen__in=list(all_sector_canteens)).values_list("id", flat=True).distinct()
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
    canteens_to_publish = []
    has_pending_actions = False

    def paginate_queryset(self, queryset, request, view=None):
        undiagnosed_canteens_with_purchases = queryset.filter(action=Canteen.Actions.PREFILL_DIAGNOSTIC).values_list(
            "pk", flat=True
        )
        self.undiagnosed_canteens_with_purchases = set(filter(lambda x: x, undiagnosed_canteens_with_purchases))
        canteens_to_publish = queryset.filter(action=Canteen.Actions.PUBLISH).values_list("pk", flat=True)
        self.canteens_to_publish = set(filter(lambda x: x, canteens_to_publish))
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
                    ("canteens_to_publish", self.canteens_to_publish),
                    ("has_pending_actions", self.has_pending_actions),
                ]
            )
        )


class PublishedCanteenFilterSet(django_filters.FilterSet):
    min_daily_meal_count = django_filters.NumberFilter(field_name="daily_meal_count", lookup_expr="gte")
    max_daily_meal_count = django_filters.NumberFilter(field_name="daily_meal_count", lookup_expr="lte")
    production_type = ProductionTypeInFilter(field_name="production_type")

    class Meta:
        model = Canteen
        fields = (
            "department",
            "region",
            "sectors",
            "city_insee_code",
            "min_daily_meal_count",
            "max_daily_meal_count",
            "management_type",
        )


def filter_by_diagnostic_params(queryset, query_params):
    bio = query_params.get("min_portion_bio")
    combined = query_params.get("min_portion_combined")
    badge = query_params.get("badge")
    appro_badge_requested = badge == "appro"
    if bio or combined or appro_badge_requested:
        publication_year = date.today().year - 1
        qs_diag = Diagnostic.objects.filter(year=publication_year, value_total_ht__gt=0)
        if bio or appro_badge_requested:
            qs_diag = qs_diag.annotate(
                bio_share=Cast(Sum("value_bio_ht", default=0) / Sum("value_total_ht"), FloatField())
            )
            if bio:
                qs_diag = qs_diag.filter(bio_share__gte=bio)
        if combined or appro_badge_requested:
            qs_diag = qs_diag.annotate(
                combined_share=Cast(
                    (
                        Sum("value_bio_ht", default=0)
                        + Sum("value_sustainable_ht", default=0)
                        + Sum("value_externality_performance_ht", default=0)
                        + Sum("value_egalim_others_ht", default=0)
                    )
                    / Sum("value_total_ht"),
                    FloatField(),
                )
            )
            if combined:
                qs_diag = qs_diag.filter(combined_share__gte=combined)
        if appro_badge_requested:
            group_1 = [Region.guadeloupe, Region.martinique, Region.guyane, Region.la_reunion]
            group_2 = [Region.mayotte]
            qs_diag = qs_diag.filter(
                Q(combined_share__gte=0.5, bio_share__gte=0.2)
                | Q(canteen__region__in=group_1, combined_share__gte=0.2, bio_share__gte=0.05)
                | Q(canteen__department=Department.saint_martin, combined_share__gte=0.2, bio_share__gte=0.05)
                | Q(canteen__region__in=group_2, combined_share__gte=0.05, bio_share__gte=0.02)
                | Q(
                    canteen__department=Department.saint_pierre_et_miquelon,
                    combined_share__gte=0.3,
                    bio_share__gte=0.1,
                )
            ).distinct()
        canteen_ids = qs_diag.values_list("canteen", flat=True)
        canteen_sirets = qs_diag.values_list("canteen__siret", flat=True)
        queryset = queryset.exclude(redacted_appro_years__contains=[publication_year])
        return queryset.filter(Q(id__in=canteen_ids) | Q(central_producer_siret__in=canteen_sirets))
    return queryset


class PublishedCanteensView(ListAPIView):
    model = Canteen
    serializer_class = PublicCanteenPreviewSerializer
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

    def get_queryset(self):
        return Canteen.objects.publicly_visible()

    def filter_queryset(self, queryset):
        new_queryset = filter_by_diagnostic_params(queryset, self.request.query_params)
        return super().filter_queryset(new_queryset)


class PublicCanteenPreviewView(RetrieveAPIView):
    model = Canteen
    serializer_class = PublicCanteenPreviewSerializer
    queryset = Canteen.objects.filter(publication_status=Canteen.PublicationStatus.PUBLISHED)


class UserCanteensFilterSet(django_filters.FilterSet):
    production_type = ProductionTypeInFilter(field_name="production_type")


class PublishManyCanteensView(APIView):
    """
    This view allows mass publishing of canteens
    """

    permission_classes = [IsAuthenticated]
    required_scopes = ["canteen"]

    def post(self, request):
        data = request.data
        canteen_ids = data.get("ids")
        if not canteen_ids or not isinstance(canteen_ids, list):
            raise BadRequest()

        canteens = []
        bad_canteens = []
        for id in canteen_ids:
            try:
                canteen = Canteen.objects.get(pk=id)
                if canteen.managers.filter(pk=request.user.id).exists():
                    canteens.append(canteen)
                else:
                    bad_canteens.append(id)
            except Canteen.DoesNotExist:
                bad_canteens.append(id)
        for canteen in canteens:
            canteen.publication_status = Canteen.PublicationStatus.PUBLISHED
            canteen.save()
            update_change_reason_with_auth(self, canteen)
        return JsonResponse({"ids": canteen_ids, "unknown_ids": bad_canteens}, status=status.HTTP_200_OK)


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
        canteen = serializer.save()
        canteen.managers.add(self.request.user)
        update_change_reason_with_auth(self, canteen)

    def create(self, request, *args, **kwargs):
        canteen_siret = request.data.get("siret")
        error_response = check_siret_response(canteen_siret, request)
        if error_response:
            raise DuplicateException(additional_data=error_response)
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
        error_response = check_siret_response(canteen_siret, request)
        if error_response and error_response.get("id") != kwargs.get("pk"):
            raise DuplicateException(additional_data=error_response)
        return super().partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        canteen = serializer.save()
        update_change_reason_with_auth(self, canteen)


class CanteenStatusView(APIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope]
    required_scopes = ["canteen"]

    def get(self, request, *args, **kwargs):
        siret = request.parser_context.get("kwargs").get("siret")
        response = check_siret_response(siret, request) or {}
        if not response:
            token = get_token_sirene()
            response = fetch_geo_data_from_api_insee_sirene_by_siret(siret, response, token)
            city = response.get("city", None)
            postcode = response.get("postalCode", None)
            if city and postcode:
                response = fetch_geo_data_from_api_entreprise_by_siret(response)
        return JsonResponse(response, status=status.HTTP_200_OK)


def check_siret_response(canteen_siret, request):
    if canteen_siret:
        canteens = Canteen.objects.filter(siret=canteen_siret)
        if canteens.exists():
            canteen = canteens.first()
            return camelize(CanteenStatusSerializer(canteen, context={"request": request}).data)


class PublishCanteenView(APIView):
    permission_classes = [IsAuthenticated]
    required_scopes = ["canteen"]

    def post(self, request, *args, **kwargs):
        if settings.PUBLISH_BY_DEFAULT:
            raise BadRequest("Cannot publish canteen")
        try:
            data = request.data
            canteen_id = kwargs.get("pk")
            canteen = Canteen.objects.get(pk=canteen_id)
            if request.user not in canteen.managers.all():
                raise PermissionDenied()

            is_draft = canteen.publication_status == Canteen.PublicationStatus.DRAFT

            if is_draft:
                canteen.publication_status = Canteen.PublicationStatus.PUBLISHED

            canteen.update_publication_comments(data)
            canteen.save()
            update_change_reason_with_auth(self, canteen)
            serialized_canteen = FullCanteenSerializer(canteen).data
            return JsonResponse(camelize(serialized_canteen), status=status.HTTP_200_OK)

        except Canteen.DoesNotExist:
            raise ValidationError("Le cantine specifié n'existe pas")


class UnpublishCanteenView(APIView):
    permission_classes = [IsAuthenticated]
    required_scopes = ["canteen"]

    def post(self, request, *args, **kwargs):
        if settings.PUBLISH_BY_DEFAULT:
            raise BadRequest("Cannot unpublish canteen")
        try:
            data = request.data
            canteen_id = kwargs.get("pk")
            canteen = Canteen.objects.get(pk=canteen_id)
            if request.user not in canteen.managers.all():
                raise PermissionDenied()

            is_not_draft = canteen.publication_status != Canteen.PublicationStatus.DRAFT

            if is_not_draft:
                canteen.publication_status = Canteen.PublicationStatus.DRAFT

            canteen.update_publication_comments(data)
            canteen.save()
            update_change_reason_with_auth(self, canteen)
            serialized_canteen = FullCanteenSerializer(canteen).data
            return JsonResponse(camelize(serialized_canteen), status=status.HTTP_200_OK)

        except Canteen.DoesNotExist:
            raise ValidationError("Le cantine specifié n'existe pas")


def _respond_with_team(canteen):
    data = ManagingTeamSerializer(canteen).data
    return JsonResponse(camelize(data), status=status.HTTP_200_OK)


class AddManagerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email").strip() if request.data.get("email") else None
            validate_email(email)
            canteen_id = request.data.get("canteen_id")
            canteen = request.user.canteens.get(id=canteen_id)
            AddManagerView.add_manager_to_canteen(email, canteen)
            return _respond_with_team(canteen)
        except ValidationError as e:
            logger.warning(f"Attempt to add manager with invalid email {email}:\n{e}")
            return JsonResponse({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        except Canteen.DoesNotExist as e:
            logger.warning(f"Attempt to add manager to unexistent canteen {canteen_id}:\n{e}")
            return JsonResponse({"error": "Invalid canteen id"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            logger.warning(f"Attempt to add existing manager with email {email} to canteen {canteen_id}:\n{e}")
            return _respond_with_team(canteen)
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
            return _respond_with_team(canteen)
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


def badges_for_queryset(diagnostic_year_queryset):
    badge_querysets = {}
    appro_total = diagnostic_year_queryset
    appro_total = diagnostic_year_queryset.count()
    if appro_total:
        appro_share_query = diagnostic_year_queryset.filter(value_total_ht__gt=0)
        appro_share_query = appro_share_query.annotate(
            bio_share=Cast(
                Sum("value_bio_ht", default=0) / Sum("value_total_ht"),
                FloatField(),
            )
        )
        appro_share_query = appro_share_query.annotate(
            combined_share=Cast(
                (
                    Sum("value_bio_ht", default=0)
                    + Sum("value_sustainable_ht", default=0)
                    + Sum("value_externality_performance_ht", default=0)
                    + Sum("value_egalim_others_ht", default=0)
                )
                / Sum("value_total_ht"),
                FloatField(),
            )
        )
        # Saint-Martin should be in group 1
        group_1 = [Region.guadeloupe, Region.martinique, Region.guyane, Region.la_reunion]
        group_2 = [Region.mayotte]
        # should have a group 3 with Saint-Pierre-et-Miquelon
        badge_querysets["appro"] = appro_share_query.filter(
            Q(combined_share__gte=0.5, bio_share__gte=0.2)
            | Q(canteen__region__in=group_1, combined_share__gte=0.2, bio_share__gte=0.05)
            | Q(canteen__department=Department.saint_martin, combined_share__gte=0.2, bio_share__gte=0.05)
            | Q(canteen__region__in=group_2, combined_share__gte=0.05, bio_share__gte=0.02)
            | Q(canteen__department=Department.saint_pierre_et_miquelon, combined_share__gte=0.3, bio_share__gte=0.1)
        ).distinct()

    # waste
    waste_badge_query = diagnostic_year_queryset.filter(has_waste_diagnostic=True)
    waste_badge_query = waste_badge_query.annotate(waste_actions_len=Func(F("waste_actions"), function="CARDINALITY"))
    waste_badge_query = waste_badge_query.filter(waste_actions_len__gt=0)
    waste_badge_query = waste_badge_query.filter(
        Q(canteen__daily_meal_count__lt=3000) | Q(has_donation_agreement=True)
    )
    badge_querysets["waste"] = waste_badge_query

    # diversification
    diversification_badge_query = diagnostic_year_queryset.exclude(vegetarian_weekly_recurrence__isnull=True)
    diversification_badge_query = diversification_badge_query.exclude(vegetarian_weekly_recurrence="")
    diversification_badge_query = diversification_badge_query.exclude(
        vegetarian_weekly_recurrence=Diagnostic.MenuFrequency.LOW
    )
    scolaire_sectors = Sector.objects.filter(category="education")
    if scolaire_sectors.count():
        diversification_badge_query = diversification_badge_query.filter(
            Q(
                canteen__sectors__in=scolaire_sectors,
                vegetarian_weekly_recurrence__in=[
                    Diagnostic.MenuFrequency.MID,
                    Diagnostic.MenuFrequency.HIGH,
                ],
            )
            | Q(vegetarian_weekly_recurrence=Diagnostic.MenuFrequency.DAILY)
        ).distinct()
    badge_querysets["diversification"] = diversification_badge_query

    # plastic
    badge_querysets["plastic"] = diagnostic_year_queryset.filter(
        cooking_plastic_substituted=True,
        serving_plastic_substituted=True,
        plastic_bottles_substituted=True,
        plastic_tableware_substituted=True,
    )

    # info
    badge_querysets["info"] = diagnostic_year_queryset.filter(communicates_on_food_quality=True)
    return badge_querysets


class CanteenStatisticsView(APIView):
    def get(self, request):
        regions = request.query_params.getlist("region")
        departments = request.query_params.getlist("department")
        sector_categories = request.query_params.getlist("sectors")
        epcis = request.query_params.getlist("epci")
        city_insee_codes = None
        year = request.query_params.get("year")
        if not year:
            return JsonResponse({"error": "Expected year"}, status=status.HTTP_400_BAD_REQUEST)

        data = {}
        try:
            city_insee_codes = CanteenStatisticsView._get_city_insee_codes(epcis)
        except Exception as e:
            logger.warning(f"Error when fetching INSEE codes for EPCI for canteen stats: {str(e)}")
            data["epci_error"] = "Une erreur est survenue"

        canteens = CanteenStatisticsView._filter_canteens(regions, departments, city_insee_codes, sector_categories)
        data["canteen_count"] = canteens.count()
        data["published_canteen_count"] = canteens.publicly_visible().count()

        diagnostics = CanteenStatisticsView._filter_diagnostics(
            year, regions, departments, city_insee_codes, sector_categories
        )

        appro_share_query = diagnostics.filter(value_total_ht__gt=0)
        appro_share_query = appro_share_query.annotate(
            bio_share=Cast(Sum("value_bio_ht", default=0) / Sum("value_total_ht"), FloatField())
        )
        appro_share_query = appro_share_query.annotate(
            sustainable_share=Cast(
                (
                    Sum("value_sustainable_ht", default=0)
                    + Sum("value_externality_performance_ht", default=0)
                    + Sum("value_egalim_others_ht", default=0)
                )
                / Sum("value_total_ht"),
                FloatField(),
            )
        )
        agg = appro_share_query.aggregate(Avg("bio_share"), Avg("sustainable_share"))
        # no need for particularly fancy rounding
        data["bio_percent"] = int((agg["bio_share__avg"] or 0) * 100)
        data["sustainable_percent"] = int((agg["sustainable_share__avg"] or 0) * 100)

        # --- badges ---
        total_diag = diagnostics.count()
        data["diagnostics_count"] = total_diag
        data["approPercent"] = 0
        data["wastePercent"] = 0
        data["diversificationPercent"] = 0
        data["plasticPercent"] = 0
        data["infoPercent"] = 0

        if total_diag:  # maybe we shouldn't be able to get to 0 diags this point with the endpoint?
            badge_querysets = badges_for_queryset(diagnostics)
            data["approPercent"] = int(badge_querysets["appro"].count() / total_diag * 100)
            data["wastePercent"] = int(badge_querysets["waste"].count() / total_diag * 100)
            data["diversificationPercent"] = int(badge_querysets["diversification"].count() / total_diag * 100)
            data["plasticPercent"] = int(badge_querysets["plastic"].count() / total_diag * 100)
            data["infoPercent"] = int(badge_querysets["info"].count() / total_diag * 100)

        # count breakdown by sector category
        sector_categories = {}
        for category in Sector.Categories:
            sectors = Sector.objects.filter(category=category)
            sector_categories[category] = canteens.filter(sectors__in=sectors).count()
        sectors = Sector.objects.filter(category=None)
        sector_categories["inconnu"] = canteens.filter(sectors__in=sectors).count()
        data["sector_categories"] = sector_categories
        return JsonResponse(camelize(data), status=status.HTTP_200_OK)

    def _get_city_insee_codes(epcis):
        city_insee_codes = []
        for e in epcis:
            response = requests.get(f"https://geo.api.gouv.fr/epcis/{e}/communes?fields=code", timeout=5)
            response.raise_for_status()
            body = response.json()
            for commune in body:
                city_insee_codes.append(commune["code"])
        return city_insee_codes

    def _filter_canteens(regions, departments, city_insee_codes, sectors):
        canteens = Canteen.objects
        if city_insee_codes:
            canteens = canteens.filter(city_insee_code__in=city_insee_codes)
        elif departments:
            canteens = canteens.filter(department__in=departments)
        elif regions:
            canteens = canteens.filter(region__in=regions)
        if sectors:
            sectors = [s for s in sectors if s.isdigit()]
            canteens = canteens.filter(sectors__in=sectors)
        return canteens.distinct()

    def _filter_diagnostics(year, regions, departments, city_insee_codes, sectors):
        diagnostics = Diagnostic.objects.filter(year=year)
        if city_insee_codes:
            diagnostics = diagnostics.filter(canteen__city_insee_code__in=city_insee_codes)
        elif departments:
            diagnostics = diagnostics.filter(canteen__department__in=departments)
        elif regions:
            diagnostics = diagnostics.filter(canteen__region__in=regions)
        if sectors:
            diagnostics = diagnostics.filter(canteen__sectors__in=sectors)
        return diagnostics.distinct()


class CanteenLocationsView(APIView):
    def get(self, _):
        canteens = Canteen.objects
        data = {}
        data["regions"] = (
            canteens.filter(region__isnull=False)
            .exclude(region="")
            .order_by("region")
            .distinct("region")
            .values_list("region", flat=True)
        )
        data["departments"] = (
            canteens.filter(department__isnull=False)
            .exclude(department="")
            .order_by("department")
            .distinct("department")
            .values_list("department", flat=True)
        )
        return JsonResponse(camelize(data), status=status.HTTP_200_OK)


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
        return JsonResponse(camelize(MinimalCanteenSerializer(canteen).data), status=status.HTTP_200_OK)


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


class SatellitesPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 40
    unpublished_count = None
    satellites_to_publish = []

    def paginate_queryset(self, queryset, request, view=None):
        unpublished_satellites = queryset.filter(publication_status=Canteen.PublicationStatus.DRAFT).only(
            "pk", "managers"
        )
        self.unpublished_count = unpublished_satellites.count()
        self.satellites_to_publish = []
        for satellite in unpublished_satellites:
            if satellite.managers.filter(pk=request.user.pk).exists():
                self.satellites_to_publish.append(satellite.id)
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                    ("unpublished_count", self.unpublished_count),
                    ("satellites_to_publish", self.satellites_to_publish),
                ]
            )
        )


@extend_schema_view(
    get=extend_schema(
        summary="Lister les cantines satellites pour une cuisine centrale.",
        description="Si la cantine en question est une cuisine centrale, cet endpoint permet de lister toutes les cantines satellites attachées à elle.",
    ),
    post=extend_schema(
        summary="Ajouter une cantine satellite à la cuisine centrale.",
        description="Si la cantine en question est une cuisine centrale, cet endpoint permet d'en ajouter une cantine satellite.",
    ),
)
class SatelliteListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    required_scopes = ["canteen"]
    model = Canteen
    serializer_class = SatelliteCanteenSerializer
    pagination_class = SatellitesPagination
    filter_backends = [
        MaCantineOrderingFilter,
    ]

    ordering_fields = [
        "name",
        "siret",
        "daily_meal_count",
        "publication_status",
    ]

    def get_queryset(self):
        canteen_pk = self.kwargs["canteen_pk"]
        return Canteen.objects.only("siret").get(pk=canteen_pk).satellites

    def post(self, request, canteen_pk):
        canteen = Canteen.objects.get(pk=canteen_pk)
        siret_satellite = request.data.get("siret")
        created = False

        if not canteen.is_central_cuisine:
            raise PermissionDenied("Votre cantine n'est pas une cuisine centrale")

        if request.user not in canteen.managers.all():
            raise PermissionDenied("Vous n'êtes pas gestionnaire de cette cantine")

        try:
            if siret_satellite and Canteen.objects.filter(siret=siret_satellite).exists():
                satellite = Canteen.objects.filter(siret=siret_satellite).first()

                if satellite.is_central_cuisine:
                    raise PermissionDenied("La cantine renseignée est une cuisine centrale")

                if satellite.central_producer_siret and satellite.central_producer_siret != canteen.siret:
                    raise PermissionDenied("Cette cantine est déjà fourni par une autre cuisine centrale")

                satellite.central_producer_siret = canteen.siret
                satellite.production_type = Canteen.ProductionType.ON_SITE_CENTRAL
                satellite.save()
                update_change_reason_with_auth(self, satellite)
            else:
                new_satellite = FullCanteenSerializer(data=request.data)
                new_satellite.is_valid(raise_exception=True)
                created = True

                satellite = new_satellite.save(
                    central_producer_siret=canteen.siret,
                    publication_status=Canteen.PublicationStatus.PUBLISHED,
                    import_source=f"Cuisine centrale : {canteen.siret}",
                    production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
                )
                update_change_reason_with_auth(self, satellite)
            if created or satellite.managers.count() == 0:
                for manager in canteen.managers.all():
                    satellite.managers.add(manager)
            serialized_canteen = FullCanteenSerializer(satellite).data
            return_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return JsonResponse(camelize(serialized_canteen), status=return_status)
        except Sector.DoesNotExist:
            raise BadRequest()


@extend_schema_view(
    post=extend_schema(
        summary="Enlever une cantine satellite à la cuisine centrale.",
        description="Cet endpoint permet d'enlever un satellite d'une cuisine centrale",
    ),
)
class UnlinkSatelliteView(APIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    serializer_class = FullCanteenSerializer

    def post(self, request, canteen_pk, satellite_pk):
        central_kitchen = Canteen.objects.get(pk=canteen_pk)

        try:
            satellite = Canteen.objects.get(pk=satellite_pk)
        except Canteen.DoesNotExist:
            serialized_canteen = FullCanteenSerializer(central_kitchen).data
            return JsonResponse(camelize(serialized_canteen), status=status.HTTP_200_OK)

        if satellite.central_producer_siret != central_kitchen.siret:
            serialized_canteen = FullCanteenSerializer(central_kitchen).data
            return JsonResponse(camelize(serialized_canteen), status=status.HTTP_200_OK)

        satellite.central_producer_siret = None
        satellite.save()
        serialized_canteen = FullCanteenSerializer(central_kitchen).data
        return JsonResponse(camelize(serialized_canteen), status=status.HTTP_200_OK)


class ActionableCanteensListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    model = Canteen
    serializer_class = CanteenActionsSerializer
    pagination_class = CanteenActionsPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
        MaCantineOrderingFilter,
    ]
    search_fields = ["name"]
    ordering_fields = ["name", "production_type", "action", "modification_date"]
    ordering = "modification_date"

    def get_queryset(self):
        year = self.request.parser_context.get("kwargs").get("year")
        return ActionableCanteensListView.annotate_actions(self.request.user.canteens, year)

    def annotate_actions(queryset, year):
        # prep add satellites action
        # https://docs.djangoproject.com/en/4.1/ref/models/expressions/#using-aggregates-within-a-subquery-expression
        satellites = (
            Canteen.objects.filter(
                central_producer_siret=OuterRef("siret"),
                production_type=Canteen.ProductionType.ON_SITE_CENTRAL,
            )
            .order_by()
            .values("central_producer_siret")  # sets the groupBy for the aggregation
        )
        central_kitchen = Canteen.objects.filter(siret=OuterRef("central_producer_siret")).values("id")
        # count by id per central prod siret, then fetch that count
        satellites_count = satellites.annotate(count=Count("id")).values("count")
        user_canteens = queryset.annotate(
            nb_satellites_in_db=Subquery(satellites_count), central_kitchen_id=Subquery(central_kitchen[:1])
        )
        # prep add diag actions
        diagnostics = Diagnostic.objects.filter(
            Q(canteen=OuterRef("central_kitchen_id")) | Q(canteen=OuterRef("pk")), year=year
        )
        user_canteens = user_canteens.annotate(diagnostic_for_year=Subquery(diagnostics.values("id")[:1]))
        purchases_for_year = Purchase.objects.filter(canteen=OuterRef("pk"), date__year=year)
        user_canteens = user_canteens.annotate(has_purchases_for_year=Exists(purchases_for_year))
        is_central_cuisine_query = Q(production_type=Canteen.ProductionType.CENTRAL) | Q(
            production_type=Canteen.ProductionType.CENTRAL_SERVING
        )
        is_satellite_query = Q(production_type=Canteen.ProductionType.ON_SITE_CENTRAL)
        # prep line ministry check
        canteen_sector_relation = apps.get_model(app_label="data", model_name="Canteen_sectors")
        has_sector_requiring_line_ministry = canteen_sector_relation.objects.filter(
            canteen=OuterRef("pk"), sector__has_line_ministry=True
        )
        user_canteens = user_canteens.annotate(requires_line_ministry=Exists(has_sector_requiring_line_ministry))
        incomplete_canteen_data_query = (
            Q(yearly_meal_count=None)
            | Q(daily_meal_count=None)
            | Q(siret=None)
            | Q(siret="")
            | Q(name=None)
            | Q(city_insee_code=None)
            | Q(city_insee_code="")
            | Q(production_type=None)
            | Q(management_type=None)
            | Q(economic_model=None)
            | (is_central_cuisine_query & Q(satellite_canteens_count=None))
            | (is_satellite_query & (Q(central_producer_siret=None) | Q(central_producer_siret="")))
            | (is_satellite_query & Q(central_producer_siret=F("siret")))
            | (Q(line_ministry=None) & Q(requires_line_ministry=True))
        )

        # prep complete diag action
        complete_diagnostics = Diagnostic.objects.filter(pk=OuterRef("diagnostic_for_year"), value_total_ht__gt=0)
        user_canteens = user_canteens.annotate(has_complete_diag=Exists(Subquery(complete_diagnostics)))
        has_cc_mode = Diagnostic.objects.filter(
            pk=OuterRef("diagnostic_for_year"),
            central_kitchen_diagnostic_mode__isnull=False,
        ).exclude(central_kitchen_diagnostic_mode="")
        user_canteens = user_canteens.annotate(has_cc_mode=Exists(Subquery(has_cc_mode)))
        # prep TD action
        tds = Teledeclaration.objects.filter(
            Q(canteen=OuterRef("pk")) | Q(canteen=OuterRef("central_kitchen_id")),
            year=year,
            status=Teledeclaration.TeledeclarationStatus.SUBMITTED,
        )
        user_canteens = user_canteens.annotate(has_td=Exists(Subquery(tds)))
        # annotate with action

        should_teledeclare = settings.ENABLE_TELEDECLARATION
        conditions = [
            When(
                (Q(satellite_canteens_count__gt=0) & Q(nb_satellites_in_db=None) & is_central_cuisine_query),
                then=Value(Canteen.Actions.ADD_SATELLITES),
            ),
            When(nb_satellites_in_db__lt=F("satellite_canteens_count"), then=Value(Canteen.Actions.ADD_SATELLITES)),
            When(nb_satellites_in_db__gt=F("satellite_canteens_count"), then=Value(Canteen.Actions.ADD_SATELLITES)),
            When(
                Q(diagnostic_for_year=None) & Q(has_purchases_for_year=True),
                then=Value(Canteen.Actions.PREFILL_DIAGNOSTIC),
            ),
            When(diagnostic_for_year=None, then=Value(Canteen.Actions.CREATE_DIAGNOSTIC)),
            When(has_complete_diag=False, then=Value(Canteen.Actions.COMPLETE_DIAGNOSTIC)),
            When((is_central_cuisine_query & Q(has_cc_mode=False)), then=Value(Canteen.Actions.COMPLETE_DIAGNOSTIC)),
            When(incomplete_canteen_data_query, then=Value(Canteen.Actions.FILL_CANTEEN_DATA)),
        ]
        if should_teledeclare:
            conditions.append(When(has_td=False, then=Value(Canteen.Actions.TELEDECLARE)))
        if not settings.PUBLISH_BY_DEFAULT:
            conditions.append(
                When(publication_status=Canteen.PublicationStatus.DRAFT, then=Value(Canteen.Actions.PUBLISH))
            )
        user_canteens = user_canteens.annotate(action=Case(*conditions, default=Value(Canteen.Actions.NOTHING)))
        return user_canteens


class ActionableCanteenRetrieveView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsCanteenManager]
    model = Canteen
    serializer_class = CanteenActionsSerializer
    required_scopes = ["canteen"]

    def get_queryset(self):
        year = self.request.parser_context.get("kwargs").get("year")
        canteen_id = self.request.parser_context.get("kwargs").get("pk")
        single_canteen_queryset = self.request.user.canteens.filter(id=canteen_id)
        return ActionableCanteensListView.annotate_actions(single_canteen_queryset, year)


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
    ordering_fields = ["name", "city", "siret", "daily_meal_count", "publication_status"]

    def get_queryset(self):
        departments = self.request.user.departments
        return Canteen.objects.filter(department__in=departments)


@extend_schema_view(
    get=extend_schema(
        summary="Lister les options pour le ministère de tutelle.",
        description="Certains secteurs nécessite la spécification d'un ministère du tutelle.",
    ),
)
class CanteenMinistriesView(APIView):
    include_in_documentation = True
    required_scopes = ["canteen"]

    def get(self, request, format=None):
        ministries = []
        for ministry in Canteen.Ministries:
            ministries.append(
                {
                    "value": ministry.value,
                    "name": ministry.label,
                }
            )
        return Response(ministries)
