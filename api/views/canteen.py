import logging
from collections import OrderedDict
from datetime import date
from django.conf import settings
from django.http import JsonResponse
from common.utils import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.db.models.functions import Cast
from django.db.models import Sum, FloatField, Avg, Func, F, Q
from django_filters import rest_framework as django_filters
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import status, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers import (
    PublicCanteenSerializer,
    FullCanteenSerializer,
    CanteenPreviewSerializer,
    ManagingTeamSerializer,
)
from data.models import Canteen, ManagerInvitation, Sector, Diagnostic
from data.region_choices import Region
from api.permissions import IsCanteenManager, IsAuthenticated, IsAuthenticatedOrTokenHasResourceScope
from api.exceptions import DuplicateException
from .utils import camelize, UnaccentSearchFilter
from common import utils

logger = logging.getLogger(__name__)


class CanteensPagination(LimitOffsetPagination):
    default_limit = 12
    max_limit = 30
    departments = []
    sectors = []
    management_types = []

    def paginate_queryset(self, queryset, request, view=None):
        # Performance improvements possible
        self.departments = set(filter(lambda x: x, queryset.values_list("department", flat=True)))
        self.regions = set(filter(lambda x: x, queryset.values_list("region", flat=True)))
        self.management_types = set(filter(lambda x: x, queryset.values_list("management_type", flat=True)))

        published_canteens = Canteen.objects.filter(publication_status="published")
        query_params = request.query_params

        if query_params.get("department"):
            published_canteens = published_canteens.filter(department=query_params.get("department"))

        if query_params.get("region"):
            published_canteens = published_canteens.filter(region=query_params.get("region"))

        if query_params.get("min_daily_meal_count"):
            published_canteens = published_canteens.filter(
                daily_meal_count__gte=query_params.get("min_daily_meal_count")
            )

        if query_params.get("max_daily_meal_count"):
            published_canteens = published_canteens.filter(
                daily_meal_count__lte=query_params.get("max_daily_meal_count")
            )

        if query_params.get("management_type"):
            published_canteens = published_canteens.filter(management_type=query_params.get("management_type"))

        published_canteens = filter_by_diagnostic_params(published_canteens, query_params)

        self.sectors = (
            Sector.objects.filter(canteen__in=list(published_canteens)).values_list("id", flat=True).distinct()
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
                ]
            )
        )


class PublishedCanteenFilterSet(django_filters.FilterSet):
    min_daily_meal_count = django_filters.NumberFilter(field_name="daily_meal_count", lookup_expr="gte")
    max_daily_meal_count = django_filters.NumberFilter(field_name="daily_meal_count", lookup_expr="lte")

    class Meta:
        model = Canteen
        fields = (
            "department",
            "region",
            "sectors",
            "min_daily_meal_count",
            "max_daily_meal_count",
            "management_type",
        )


def filter_by_diagnostic_params(queryset, query_params):
    bio = query_params.get("min_portion_bio")
    combined = query_params.get("min_portion_combined")
    if bio or combined:
        publication_year = date.today().year - 1
        qs_diag = Diagnostic.objects.filter(year=publication_year, value_total_ht__gt=0)
        if bio:
            qs_diag = qs_diag.annotate(
                bio_share=Cast(Sum("value_bio_ht") / Sum("value_total_ht"), FloatField())
            ).filter(bio_share__gte=bio)
        if combined:
            qs_diag = qs_diag.annotate(
                combined_share=Cast(
                    (Sum("value_bio_ht") + Sum("value_sustainable_ht")) / Sum("value_total_ht"),
                    FloatField(),
                )
            ).filter(combined_share__gte=combined)
        canteen_ids = qs_diag.values_list("canteen", flat=True)
        return queryset.filter(id__in=canteen_ids)
    return queryset


class PublishedCanteensView(ListAPIView):
    model = Canteen
    serializer_class = PublicCanteenSerializer
    queryset = Canteen.objects.filter(publication_status=Canteen.PublicationStatus.PUBLISHED)
    pagination_class = CanteensPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
        UnaccentSearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name"]
    ordering_fields = ["name", "creation_date", "modification_date", "daily_meal_count"]
    filterset_class = PublishedCanteenFilterSet

    def filter_queryset(self, queryset):
        new_queryset = filter_by_diagnostic_params(queryset, self.request.query_params)
        return super().filter_queryset(new_queryset)


class PublishedCanteenSingleView(RetrieveAPIView):
    model = Canteen
    serializer_class = PublicCanteenSerializer
    queryset = Canteen.objects.filter(publication_status="published")


class UserCanteensView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope]
    model = Canteen
    serializer_class = FullCanteenSerializer
    pagination_class = CanteensPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
        UnaccentSearchFilter,
        filters.OrderingFilter,
    ]
    required_scopes = ["canteen"]
    search_fields = ["name"]
    ordering_fields = ["name", "creation_date", "modification_date", "daily_meal_count"]

    def get_serializer(self, *args, **kwargs):
        kwargs.setdefault("context", self.get_serializer_context())
        action = "create" if self.request.method == "POST" else None
        kwargs.setdefault("action", action)
        return FullCanteenSerializer(*args, **kwargs)

    def get_queryset(self):
        return self.request.user.canteens.all()

    def perform_create(self, serializer):
        canteen = serializer.save()
        canteen.managers.add(self.request.user)

    def create(self, request, *args, **kwargs):
        error_response = check_siret_response(request)
        if error_response:
            return error_response
        return super().create(request, *args, **kwargs)


class UserCanteenPreviews(ListAPIView):
    model = Canteen
    serializer_class = CanteenPreviewSerializer
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope]
    required_scopes = ["canteen"]

    def get_queryset(self):
        return self.request.user.canteens.all()


class RetrieveUpdateUserCanteenView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsCanteenManager]
    model = Canteen
    serializer_class = FullCanteenSerializer
    queryset = Canteen.objects.all()
    required_scopes = ["canteen"]

    def put(self, request, *args, **kwargs):
        return JsonResponse({"error": "Only PATCH request supported in this resource"}, status=405)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        error_response = check_siret_response(request)
        if error_response:
            return error_response
        return super().partial_update(request, *args, **kwargs)


def check_siret_response(request):
    canteen_siret = request.data.get("siret")
    if canteen_siret:
        canteens = Canteen.objects.filter(siret=canteen_siret)
        if canteens.exists():
            canteen = canteens.first()
            managed_by_user = request.user in canteen.managers.all()
            raise DuplicateException(
                additional_data={"name": canteen.name, "id": canteen.id, "isManagedByUser": managed_by_user}
            )


class PublishCanteenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            canteen_id = kwargs.get("pk")
            canteen = Canteen.objects.get(pk=canteen_id)
            if request.user not in canteen.managers.all():
                raise PermissionDenied()

            is_draft = canteen.publication_status == Canteen.PublicationStatus.DRAFT

            if is_draft:
                canteen.publication_status = Canteen.PublicationStatus.PENDING
                protocol = settings.PROTOCOL
                admin_url = "{}://{}/admin/data/canteen/{}/change/".format(protocol, settings.HOSTNAME, canteen.id)

                logger.info(f"Demande de publication de {canteen.name} (ID: {canteen.id})")

                title = canteen.name
                env = getattr(settings, "ENVIRONMENT", "")
                if env == "demo" or env == "staging":
                    title = f"({env.upper()}) {title}"

                description = f"[admin]({admin_url})"
                if canteen.sectors.count():
                    description += "\n\nSecteurs\n"
                    for sector in canteen.sectors.all().order_by("name"):
                        description += f"\n* {sector.name}"
                else:
                    description += "\n\nAucun secteur"
                utils.create_trello_card(settings.TRELLO_LIST_ID_PUBLICATION, title, description)

            canteen.update_publication_comments(data)
            canteen.save()
            serialized_canteen = FullCanteenSerializer(canteen).data
            return JsonResponse(camelize(serialized_canteen), status=status.HTTP_200_OK)

        except Canteen.DoesNotExist:
            raise ValidationError("Le cantine specifié n'existe pas")


class UnpublishCanteenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
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
            logger.error(f"Attempt to add manager with invalid email {email}")
            logger.exception(e)
            return JsonResponse({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        except Canteen.DoesNotExist as e:
            logger.error(f"Attempt to add manager to unexistent canteen {canteen_id}")
            logger.exception(e)
            return JsonResponse({"error": "Invalid canteen id"}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            logger.error(f"Attempt to add existing manager with email {email} to canteen {canteen_id}")
            logger.exception(e)
            return _respond_with_team(canteen)
        except Exception as e:
            logger.error("Exception ocurred while inviting a manager to canteen")
            logger.exception(e)
            return JsonResponse(
                {"error": "An error has ocurred"},
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
            logger.error(
                f"The manager invitation email could not be sent to {manager_invitation.email} : Connection Refused. The manager has been added anyway."
            )
            logger.exception(e)
            return
        except Exception as e:
            logger.error(f"The manager invitation email could not be sent to {manager_invitation.email}")
            logger.exception(e)
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
            logger.error(
                f"The manager add notification email could not be sent to {email} : Connection Refused. The manager has been added anyway."
            )
            logger.exception(e)
            return
        except Exception as e:
            logger.error(f"The manager add notification email could not be sent to {email}")
            logger.exception(e)
            raise Exception("Error occurred : the mail could not be sent.") from e


class RemoveManagerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
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
            logger.error(f"Attempt to remove manager with invalid email {email}")
            logger.exception(e)
            return JsonResponse({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        except Canteen.DoesNotExist as e:
            logger.error(f"Attempt to remove manager from unexistent canteen {canteen_id}")
            logger.exception(e)
            return JsonResponse({"error": "Invalid canteen id"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error("Exception ocurred while removing a manager from a canteen")
            logger.exception(e)
            return JsonResponse(
                {"error": "An error has ocurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SendCanteenNotFoundEmail(APIView):
    def post(self, request):
        try:
            email = request.data.get("from")
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
            logger.error("Exception ocurred while sending email")
            logger.exception(e)
            return JsonResponse(
                {"error": "An error has ocurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class TeamJoinRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
            validate_email(email)
            name = request.data.get("name")
            message = request.data.get("message")
            canteen_id = kwargs.get("pk")
            canteen = Canteen.objects.get(pk=canteen_id)
            canteen_path = f"/modifier-ma-cantine/{canteen.url_slug}"
            url = f"{'https' if settings.SECURE else 'http'}://{settings.HOSTNAME}{canteen_path}/gestionnaires"

            context = {
                "email": email,
                "name": name,
                "message": message,
                "url": url,
                "canteen": canteen.name,
                "siret": canteen.siret,
            }

            recipients = list(canteen.managers.values_list("email", flat=True))
            cc = None

            if recipients:
                cc = [settings.CONTACT_EMAIL]
            else:
                recipients.append(settings.CONTACT_EMAIL)

            send_mail(
                subject=f"{name} voudrait rejoindre l'équipe de gestion de la cantine {canteen.name}",
                to=recipients,
                cc=cc,
                reply_to=[
                    email,
                ],
                template="canteen_join_request",
                context=context,
            )

            return JsonResponse({}, status=status.HTTP_200_OK)
        except ValidationError:
            return JsonResponse({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Exception ocurred while sending email")
            logger.exception(e)
            return JsonResponse(
                {"error": "An error has ocurred"},
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
                Sum("value_bio_ht") / Sum("value_total_ht"),
                FloatField(),
            )
        )
        appro_share_query = appro_share_query.annotate(
            combined_share=Cast(
                (Sum("value_bio_ht") + Sum("value_sustainable_ht")) / Sum("value_total_ht"),
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
            | Q(canteen__region__in=group_2, combined_share__gte=0.05, bio_share__gte=0.02)
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
        region = request.query_params.get("region")
        department = request.query_params.get("department")
        sectors = request.query_params.getlist("sectors")
        year = request.query_params.get("year")
        if not year:
            return JsonResponse({"error": "Expected year"}, status=status.HTTP_400_BAD_REQUEST)
        data = {}
        canteens = Canteen.objects
        if region:
            canteens = canteens.filter(region=region)
        elif department:
            canteens = canteens.filter(department=department)
        if sectors:
            sectors = [s for s in sectors if s.isdigit()]
            canteens = canteens.filter(sectors__in=sectors)
        data["canteen_count"] = canteens.count()
        data["published_canteen_count"] = canteens.filter(
            publication_status=Canteen.PublicationStatus.PUBLISHED
        ).count()

        diagnostics = Diagnostic.objects.filter(year=year)
        if region:
            diagnostics = diagnostics.filter(canteen__region=region)
        elif department:
            diagnostics = diagnostics.filter(canteen__department=department)
        if sectors:
            diagnostics = diagnostics.filter(canteen__sectors__in=sectors)
        appro_share_query = diagnostics.filter(value_total_ht__gt=0)
        appro_share_query = appro_share_query.annotate(
            bio_share=Cast(Sum("value_bio_ht") / Sum("value_total_ht"), FloatField())
        )
        appro_share_query = appro_share_query.annotate(
            sustainable_share=Cast(Sum("value_sustainable_ht") / Sum("value_total_ht"), FloatField())
        )
        agg = appro_share_query.aggregate(Avg("bio_share"), Avg("sustainable_share"))
        # no need for particularly fancy rounding
        data["bio_percent"] = int((agg["bio_share__avg"] or 0) * 100)
        data["sustainable_percent"] = int((agg["sustainable_share__avg"] or 0) * 100)

        # --- badges ---
        total_diag = diagnostics
        total_diag = total_diag.count()
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

        # count breakdown by sector
        sectors = {}
        for sector in Sector.objects.all():
            sectors[sector.id] = canteens.filter(sectors=sector).count()
        data["sectors"] = sectors
        return JsonResponse(camelize(data), status=status.HTTP_200_OK)


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

    def post(self, request, canteen_pk):
        try:
            canteen_name = Canteen.objects.only("name").get(pk=canteen_pk).name

            context = {
                "email": self.request.user.email,
                "name": self.request.user.get_full_name(),
                "username": self.request.user.username,
                "canteen_name": canteen_name,
                "canteen_id": canteen_pk,
                "protocol": settings.PROTOCOL,
                "domain": settings.HOSTNAME,
            }

            send_mail(
                subject=f"{self.request.user.get_full_name()} voudrait revendiquer la canteen {canteen_name}",
                to=[
                    settings.CONTACT_EMAIL,
                ],
                template="canteen_claim",
                context=context,
            )

            return JsonResponse({}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exception ocurred while sending email")
            logger.exception(e)
            return JsonResponse(
                {"error": "An error has ocurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
