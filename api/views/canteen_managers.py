import logging

from rest_framework.generics import ListAPIView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import BadRequest, ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrTokenHasResourceScope,
    IsCanteenManagerUrlParam,
)
from api.serializers import (
    ManagingTeamSerializer,
    MinimalCanteenSerializer,
    CanteenManagerSerializer,
    ManagerInvitationSerializer,
)
from common.utils import send_mail
from data.models import Canteen, ManagerInvitation

logger = logging.getLogger(__name__)


@extend_schema_view(
    get=extend_schema(
        summary="Lister les gestionnaires d'une cantine.",
        description="",
        tags=["Cantines"],
    )
)
class UserCanteenManagersView(ListAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    model = get_user_model()
    serializer_class = CanteenManagerSerializer  # ManagingTeamSerializer

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def get_queryset(self):
        canteen = self._get_canteen()
        return canteen.managers.all()


class UserCanteenManagersInvitationsView(ListAPIView):
    permission_classes = [IsAuthenticatedOrTokenHasResourceScope, IsCanteenManagerUrlParam]
    model = ManagerInvitation
    serializer_class = ManagerInvitationSerializer

    def _get_canteen(self):
        # IsCanteenManagerUrlParam will raise a 404 if the canteen doesn't exist
        return Canteen.objects.get(pk=self.kwargs["canteen_pk"])

    def get_queryset(self):
        canteen = self._get_canteen()
        return canteen.managerinvitation_set.all()


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


class TeamJoinRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, canteen_pk, *args, **kwargs):
        try:
            email = request.data.get("email", "").strip()
            validate_email(email)
            name = request.data.get("name")
            message = request.data.get("message")
            canteen = Canteen.objects.get(pk=canteen_pk)
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
        canteen.save(skip_validations=True)
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
        canteen.save(skip_validations=True)
        return JsonResponse({}, status=status.HTTP_200_OK)
