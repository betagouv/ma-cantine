import logging
from collections import OrderedDict
from datetime import date
from django.conf import settings
from django.http import JsonResponse
from common.utils import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.db.models.constants import LOOKUP_SEP
from django.db.models.functions import Cast
from django.db.models import Sum, FloatField, Avg
from django_filters import rest_framework as django_filters
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework import permissions, status, filters
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
from api.permissions import IsCanteenManager
from .utils import camelize
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

        sector_queryset = Canteen.objects.filter(publication_status="published")
        query_params = request.query_params

        if query_params.get("department"):
            sector_queryset = sector_queryset.filter(department=query_params.get("department"))

        if query_params.get("region"):
            sector_queryset = sector_queryset.filter(region=query_params.get("region"))

        if query_params.get("min_daily_meal_count"):
            sector_queryset = sector_queryset.filter(daily_meal_count__gte=query_params.get("min_daily_meal_count"))

        if query_params.get("max_daily_meal_count"):
            sector_queryset = sector_queryset.filter(daily_meal_count__lte=query_params.get("max_daily_meal_count"))

        if query_params.get("management_type"):
            sector_queryset = sector_queryset.filter(management_type=query_params.get("management_type"))

        sector_queryset = filter_by_diagnostic_params(sector_queryset, query_params)

        self.sectors = Sector.objects.filter(canteen__in=list(sector_queryset)).values_list("id", flat=True).distinct()
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


class UnaccentSearchFilter(filters.SearchFilter):
    def construct_search(self, field_name):
        lookup = self.lookup_prefixes.get(field_name[0])
        if lookup:
            field_name = field_name[1:]
        else:
            lookup = "icontains"
        return LOOKUP_SEP.join(
            [
                field_name,
                "unaccent",
                lookup,
            ]
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
    permission_classes = [permissions.IsAuthenticated]
    model = Canteen
    serializer_class = FullCanteenSerializer
    pagination_class = CanteensPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
        UnaccentSearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name"]
    ordering_fields = ["name", "creation_date", "modification_date", "daily_meal_count"]

    def get_queryset(self):
        return self.request.user.canteens.all()

    def perform_create(self, serializer):
        canteen = serializer.save()
        canteen.managers.add(self.request.user)


class UserCanteenPreviews(ListAPIView):
    model = Canteen
    serializer_class = CanteenPreviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.canteens.all()


class RetrieveUpdateUserCanteenView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCanteenManager]
    model = Canteen
    serializer_class = FullCanteenSerializer
    queryset = Canteen.objects.all()

    def put(self, request, *args, **kwargs):
        return JsonResponse({"error": "Only PATCH request supported in this resource"}, status=405)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class PublishCanteenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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
                protocol = "https" if settings.SECURE else "http"
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
    permission_classes = [permissions.IsAuthenticated]

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
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
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
    def add_manager_to_canteen(email, canteen):
        try:
            user = get_user_model().objects.get(email=email)
            canteen.managers.add(user)
        except get_user_model().DoesNotExist:
            with transaction.atomic():
                pm = ManagerInvitation(canteen_id=canteen.id, email=email)
                pm.save()
            AddManagerView._send_invitation_email(pm)

    @staticmethod
    def _send_invitation_email(manager_invitation):
        try:
            context = {
                "canteen": manager_invitation.canteen.name,
                "protocol": "https" if settings.SECURE_SSL_REDIRECT else "http",
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


class RemoveManagerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

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


class SendCanteenEmailView(APIView):
    def post(self, request):
        try:
            email = request.data.get("from")
            validate_email(email)

            canteen_id = request.data.get("canteen_id")
            canteen = Canteen.objects.get(pk=canteen_id)

            recipients = [user.email for user in canteen.managers.all()]
            recipients.append(settings.DEFAULT_FROM_EMAIL)

            reply_to = [email]  # SendinBlue does not support multiple reply_to addresses

            context = {
                "canteen": canteen.name,
                "from": email,
                "name": request.data.get("name") or "Une personne",
                "message": request.data.get("message"),
                "us": settings.DEFAULT_FROM_EMAIL,
            }

            send_mail(
                subject=f"Un message pour {canteen.name}",
                to=recipients,
                reply_to=reply_to,
                template="contact_canteen",
                context=context,
            )

            return JsonResponse({}, status=status.HTTP_200_OK)
        except ValidationError:
            return JsonResponse({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Invalid canteen"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("Exception ocurred while sending email to published canteen")
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
                "us": settings.DEFAULT_FROM_EMAIL,
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


class CanteenStatisticsView(APIView):
    def get(self, request):
        region = request.query_params.get("region")
        department = request.query_params.get("department")
        year = request.query_params.get("year")
        if not year or (not region and not department):
            return JsonResponse(
                {"error": "Expected both year and one of region or department"}, status=status.HTTP_400_BAD_REQUEST
            )
        data = {}
        canteens = None
        if region:
            canteens = Canteen.objects.filter(region=region)
        elif department:
            canteens = Canteen.objects.filter(department=department)
        data["canteen_count"] = canteens.count()
        data["published_canteen_count"] = canteens.filter(
            publication_status=Canteen.PublicationStatus.PUBLISHED
        ).count()

        diagnostics = Diagnostic.objects.filter(year=year)
        if region:
            diagnostics = diagnostics.filter(canteen__region=region)
        elif department:
            diagnostics = diagnostics.filter(canteen__department=department)
        qs_diag = diagnostics.filter(value_total_ht__gt=0)
        qs_diag = qs_diag.annotate(bio_share=Cast(Sum("value_bio_ht") / Sum("value_total_ht"), FloatField()))
        qs_diag = qs_diag.annotate(
            sustainable_share=Cast(Sum("value_sustainable_ht") / Sum("value_total_ht"), FloatField())
        )
        agg = qs_diag.aggregate(Avg("bio_share"), Avg("sustainable_share"))
        # no need for particularly fancy rounding
        data["bio_percent"] = int((agg["bio_share__avg"] or 0) * 100)
        data["sustainable_percent"] = int((agg["sustainable_share__avg"] or 0) * 100)
        return JsonResponse(camelize(data), status=status.HTTP_200_OK)
