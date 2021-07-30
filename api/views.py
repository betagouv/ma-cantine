import logging
from data.models.diagnostic import Diagnostic
import json
from django.contrib.auth import get_user_model, update_session_auth_hash, tokens
from django.conf import settings
from django.db import transaction, IntegrityError
from django.http import JsonResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.exceptions import (
    ObjectDoesNotExist,
    ValidationError,
    BadRequest,
)
from django.core.validators import validate_email
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView
from rest_framework.generics import (
    UpdateAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from api.serializers import LoggedUserSerializer, DiagnosticSerializer, SectorSerializer
from api.serializers import (
    PublicCanteenSerializer,
    FullCanteenSerializer,
    BlogPostSerializer,
    PasswordSerializer,
    ManagingTeamSerializer,
)
from data.models import Canteen, BlogPost, Sector, ManagerInvitation
from api.permissions import IsProfileOwner, IsCanteenManager, CanEditDiagnostic
import sib_api_v3_sdk
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
import csv
import time
import re

logger = logging.getLogger(__name__)


class LoggedUserView(RetrieveAPIView):
    model = get_user_model()
    serializer_class = LoggedUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = get_user_model().objects.all()

    def get_object(self):
        return self.request.user


class UpdateUserView(UpdateAPIView):
    model = get_user_model()
    serializer_class = LoggedUserSerializer
    permission_classes = [permissions.IsAuthenticated, IsProfileOwner]
    queryset = get_user_model().objects.all()

    def put(self, request, *args, **kwargs):
        return JsonResponse(
            {"error": "Only PATCH request supported in this resource"}, status=405
        )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        previous_email = serializer.instance.email
        new_email = serializer.validated_data.get("email", previous_email)

        update = super().perform_update(serializer)

        if previous_email != new_email:
            self.unconfirm_email(serializer.instance)
            self.send_confirmation_email(new_email, serializer.instance)

        return update

    def unconfirm_email(self, user):
        user.email_confirmed = False
        user.save()

    def send_confirmation_email(self, new_email, user):
        token = tokens.default_token_generator.make_token(user)
        html_template = "auth/account_activate_email.html"
        text_template = "auth/account_activate_email.txt"
        context = {
            "token": token,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "protocol": "https" if settings.SECURE_SSL_REDIRECT else "http",
            "domain": settings.HOSTNAME,
        }
        send_mail(
            subject="Confirmation de votre changement d'adresse email - ma cantine",
            message=render_to_string(text_template, context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            html_message=render_to_string(html_template, context),
            recipient_list=[new_email],
            fail_silently=False,
        )


class PublishedCanteensPagination(LimitOffsetPagination):
    default_limit = 12
    max_limit = 30


class PublishedCanteensView(ListAPIView):
    model = Canteen
    serializer_class = PublicCanteenSerializer
    queryset = Canteen.objects.filter(publication_status="published")
    pagination_class = PublishedCanteensPagination


class PublishedCanteenSingleView(RetrieveAPIView):
    model = Canteen
    serializer_class = PublicCanteenSerializer
    queryset = Canteen.objects.filter(publication_status="published")


class UserCanteensView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    model = Canteen
    serializer_class = FullCanteenSerializer

    def get_queryset(self):
        return self.request.user.canteens.all()

    def perform_create(self, serializer):
        canteen = serializer.save()
        canteen.managers.add(self.request.user)


class UpdateUserCanteenView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsCanteenManager]
    model = Canteen
    serializer_class = FullCanteenSerializer
    queryset = Canteen.objects.all()

    def put(self, request, *args, **kwargs):
        return JsonResponse(
            {"error": "Only PATCH request supported in this resource"}, status=405
        )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        is_draft = serializer.instance.publication_status == "draft"
        publication_requested = (
            serializer.validated_data.get("publication_status") == "pending"
        )

        if is_draft and publication_requested:
            protocol = "https" if settings.SECURE else "http"
            canteen = serializer.instance
            admin_url = "{}://{}/admin/data/canteen/{}/change/".format(
                protocol, settings.HOSTNAME, canteen.id
            )

            send_mail(
                "Demande de publication sur ma cantine",
                f"La cantine « {canteen.name} » a demandé d'être publiée.\nAdmin : {admin_url}",
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=True,
            )

        return super(UpdateUserCanteenView, self).perform_update(serializer)


class DiagnosticCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    model = Diagnostic
    serializer_class = DiagnosticSerializer

    def perform_create(self, serializer):
        try:
            canteen_id = self.request.parser_context.get("kwargs").get("canteen_pk")
            canteen = Canteen.objects.get(pk=canteen_id)
            if not IsCanteenManager().has_object_permission(
                self.request, self, canteen
            ):
                raise PermissionDenied()
            serializer.save(canteen=canteen)
        except ObjectDoesNotExist:
            raise NotFound()
        except IntegrityError:
            raise BadRequest()


class DiagnosticUpdateView(UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated, CanEditDiagnostic]
    model = Diagnostic
    serializer_class = DiagnosticSerializer
    queryset = Diagnostic.objects.all()

    def put(self, request, *args, **kwargs):
        return JsonResponse(
            {"error": "Only PATCH request supported in this resource"}, status=405
        )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class SectorListView(ListAPIView):
    model = Sector
    serializer_class = SectorSerializer
    queryset = Sector.objects.all()


class BlogPostsPagination(LimitOffsetPagination):
    default_limit = 6
    max_limit = 30


class BlogPostsView(ListAPIView):
    model = BlogPost
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.filter(published=True)
    pagination_class = BlogPostsPagination


class BlogPostView(RetrieveAPIView):
    model = BlogPost
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostSerializer


class SubscribeBetaTester(APIView):
    def post(self, request):
        try:
            data = request.data
            key_measures = request.data.get("measures", {})
            context = {
                "canteen": data.get("school"),
                "city": data.get("city"),
                "email": data["email"],
                "phone": data.get("phone", "Non renseigné"),
                "message": data.get("message", "Non renseigné"),
                "measures": key_measures,
            }
            send_mail(
                "Nouveau Béta-testeur ma cantine",
                render_to_string("subscription-beta-tester.txt", context),
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                html_message=render_to_string("subscription-beta-tester.html", context),
            )
            return JsonResponse({}, status=status.HTTP_201_CREATED)
        except Exception:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)


class SubscribeNewsletter(APIView):
    def post(self, request):
        try:
            email = request.data.get("email")
            validate_email(email)

            list_id = settings.NEWSLETTER_SENDINBLUE_LIST_ID
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key["api-key"] = settings.ANYMAIL.get(
                "SENDINBLUE_API_KEY"
            )
            api_instance = sib_api_v3_sdk.ContactsApi(
                sib_api_v3_sdk.ApiClient(configuration)
            )
            create_contact = sib_api_v3_sdk.CreateContact(email=email)
            create_contact.list_ids = [int(list_id)]
            create_contact.update_enabled = True
            api_instance.create_contact(create_contact)
            return JsonResponse({}, status=status.HTTP_200_OK)
        except sib_api_v3_sdk.rest.ApiException as e:
            contact_exists = (
                json.loads(e.body).get("message") == "Contact already exist"
            )
            if contact_exists:
                return JsonResponse({}, status=status.HTTP_200_OK)
            return JsonResponse(
                {"error": "Error calling SendInBlue API"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError:
            return JsonResponse(
                {"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            return JsonResponse(
                {"error": "An error has ocurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ChangePasswordView(UpdateAPIView):
    serializer_class = PasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        update_session_auth_hash(
            request, request.user
        )  # After a password change Django logs the user out
        return JsonResponse({}, status=status.HTTP_200_OK)


class AddManagerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get("email")
            validate_email(email)
            canteen_id = request.data.get("canteen_id")
            canteen = request.user.canteens.get(id=canteen_id)
            try:
                user = get_user_model().objects.get(email=email)
                canteen.managers.add(user)
            except get_user_model().DoesNotExist:
                with transaction.atomic():
                    pm = ManagerInvitation(canteen_id=canteen.id, email=email)
                    pm.save()
                _send_invitation_email(pm)
            return _respond_with_team(canteen)
        except ValidationError:
            return JsonResponse(
                {"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Canteen.DoesNotExist:
            return JsonResponse(
                {"error": "Invalid canteen id"}, status=status.HTTP_404_NOT_FOUND
            )
        except IntegrityError:
            return _respond_with_team(canteen)
        except Exception:
            return JsonResponse(
                {"error": "An error has ocurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


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
                    invitation = ManagerInvitation.objects.get(
                        canteen_id=canteen.id, email=email
                    )
                    invitation.delete()
                except ManagerInvitation.DoesNotExist:
                    pass
            return _respond_with_team(canteen)
        except ValidationError:
            return JsonResponse(
                {"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Canteen.DoesNotExist:
            return JsonResponse(
                {"error": "Invalid canteen id"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return JsonResponse(
                {"error": "An error has ocurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def _respond_with_team(canteen):
    data = ManagingTeamSerializer(canteen).data
    return JsonResponse(_camelize(data), status=status.HTTP_200_OK)


def _camelize(data):
    camel_case_bytes = CamelCaseJSONRenderer().render(data)
    return json.loads(camel_case_bytes.decode("utf-8"))


def _send_invitation_email(manager_invitation):
    try:
        template = "auth/manager-invitation"
        context = {
            "canteen": manager_invitation.canteen.name,
            "protocol": "https" if settings.SECURE_SSL_REDIRECT else "http",
            "domain": settings.HOSTNAME,
        }
        send_mail(
            subject="Invitation à gérer une cantine sur ma cantine",
            message=render_to_string(f"{template}.txt", context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            html_message=render_to_string(f"{template}.html", context),
            recipient_list=[manager_invitation.email],
            fail_silently=False,
        )
    except Exception:
        raise Exception("Error occurred : the mail could not be sent.")


class SendCanteenEmailView(APIView):
    def post(self, request):
        try:
            email = request.data.get("from")
            validate_email(email)

            canteen_id = request.data.get("canteen_id")
            canteen = Canteen.objects.get(pk=canteen_id)

            template = "contact-canteen"
            context = {
                "canteen": canteen.name,
                "from": email,
                "name": request.data.get("name") or "Une personne",
                "message": request.data.get("message"),
                "us": settings.DEFAULT_FROM_EMAIL,
            }
            recipients = [user.email for user in canteen.managers.all()]
            recipients.append(settings.DEFAULT_FROM_EMAIL)

            reply_to = recipients.copy()
            reply_to.append(email)

            subject = f"Un message pour {canteen.name}"
            from_email = settings.DEFAULT_FROM_EMAIL
            html_content = render_to_string(f"{template}.html", context)
            text_content = render_to_string(f"{template}.txt", context)

            message = EmailMultiAlternatives(
                subject, text_content, from_email, recipients, reply_to=reply_to
            )
            message.attach_alternative(html_content, "text/html")
            message.send()

            return JsonResponse({}, status=status.HTTP_200_OK)
        except ValidationError:
            return JsonResponse(
                {"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST
            )
        except ObjectDoesNotExist:
            return JsonResponse(
                {"error": "Invalid canteen"}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception:
            return JsonResponse(
                {"error": "An error has ocurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


def _normalise_siret(siret):
    # TODO: find official siret format
    return siret.replace(" ", "")


def _get_verbose_field_name(field_name):
    try:
        verbose_field_name = Canteen._meta.get_field(field_name).verbose_name
    except:
        try:
            verbose_field_name = Diagnostic._meta.get_field(field_name).verbose_name
        except:
            pass
    return verbose_field_name


# flake8: noqa: C901
class ImportDiagnosticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    value_error_regex = re.compile(r"Field '(.+)' expected .+? got '(.+)'.")
    validation_error_regex = re.compile(r"La valeur «\xa0(.+)\xa0»")
    # TODO? Django adds quotes for choice validation errors so the regex would be:
    # choice_error_regex = re.compile(
    #     r"La valeur «\xa0'(.+)'\xa0» n’est pas un choix valide."
    # )

    def post(self, request):
        start = time.time()
        logger.info("Diagnostic bulk import started")
        diagnostics_created = 0
        canteens = {}
        errors = []
        try:
            filestring = request.data["file"].read().decode("utf-8")
            csvreader = csv.reader(filestring.splitlines())
            with transaction.atomic():
                for row_number, row in enumerate(csvreader, start=1):
                    try:
                        siret = _normalise_siret(row[0])
                        canteen = self._create_canteen_with_diagnostic(row, siret)
                        diagnostics_created += 1
                        canteens[canteen.siret] = canteen
                    except Exception as e:
                        (message, code) = self._parse_error(e)
                        errors.append(
                            ImportDiagnosticsView._get_error(
                                e, message, code, row_number
                            )
                        )

                if errors:
                    raise IntegrityError()

            serialized_canteens = [
                _camelize(FullCanteenSerializer(canteen).data)
                for canteen in canteens.values()
            ]
            return ImportDiagnosticsView._get_success_response(
                serialized_canteens, diagnostics_created, errors, start
            )

        except IntegrityError:
            logger.error("L'import du fichier CSV a échoué")
            return ImportDiagnosticsView._get_success_response([], 0, errors, start)

        except Exception as e:
            logger.exception(e)
            message = "Échec lors de la lecture du fichier"
            errors = [{"row": 0, "status": 400, "message": message}]
            return ImportDiagnosticsView._get_success_response([], 0, errors, start)

    @transaction.atomic
    def _create_canteen_with_diagnostic(self, row, siret):
        (canteen, created) = Canteen.objects.get_or_create(
            siret=siret,
            defaults={
                "siret": siret,
                "name": row[1],  # TODO: should this be optional or not?
                "city_insee_code": row[2],
                "postal_code": row[3],
                "central_producer_siret": row[4],
                "daily_meal_count": row[5],
                "production_type": row[7],
                "management_type": row[8],
            },
        )

        if not created and self.request.user not in canteen.managers.all():
            raise PermissionDenied()

        if created:
            canteen.managers.add(self.request.user)
            if row[6]:
                canteen.sectors.add(
                    *[Sector.objects.get(name=sector) for sector in row[6].split("+")]
                )
            canteen.full_clean()  # validate choice fields
            canteen.save()

        diagnostic = Diagnostic(
            canteen_id=canteen.id,
            year=row[9],
            value_total_ht=row[10],
            value_bio_ht=row[11],
            value_sustainable_ht=row[12],
            value_fair_trade_ht=row[13],
        )
        diagnostic.full_clean()  # trigger field validators like year min/max
        diagnostic.save()
        return canteen

    @staticmethod
    def _get_error(e, message, error_status, row_number):
        logger.error(f"Error on row {row_number}")
        logger.exception(e)
        return {"row": row_number, "status": error_status, "message": message}

    @staticmethod
    def _get_success_response(canteens, count, errors, start_time):
        return JsonResponse(
            {
                "canteens": canteens,
                "count": count,
                "errors": errors,
                "seconds": time.time() - start_time,
            },
            status=status.HTTP_200_OK,
        )

    def _parse_error(self, e):
        message = "Une erreur s'est produite en créant un diagnostic pour cette ligne"
        code = 400
        if isinstance(e, PermissionDenied):
            message = f"Vous n'êtes pas un gestionnaire de cette cantine."
            code = 401
        elif isinstance(e, Sector.DoesNotExist):
            message = "Le secteur spécifié ne fait pas partie des options acceptées"
        elif isinstance(e, ValidationError):
            try:
                field_name = list(e.message_dict.keys())[0]
                if (
                    hasattr(e, "messages")
                    and e.messages[0]
                    == "Un objet Diagnostic avec ces champs Canteen et An existe déjà."
                ):
                    message = (
                        "Un diagnostic pour cette année et cette cantine existe déjà"
                    )
                elif field_name:
                    verbose_field_name = _get_verbose_field_name(field_name)
                    match = self.validation_error_regex.search(e.messages[0])
                    if match:
                        value_given = match.group(1) if match else ""
                        message = f"La valeur '{value_given}' n'est pas valide pour le champ '{verbose_field_name}'."
                    elif field_name == "year":
                        message = (
                            f"Pour le champ '{verbose_field_name}', {e.messages[0]}"
                        )
            except:
                if hasattr(e, "params"):
                    message = f"La valeur '{e.params['value']}' n'est pas valide."
        elif isinstance(e, ValueError):
            match = self.value_error_regex.search(str(e))
            field_name = match.group(1) if match else ""
            value_given = match.group(2) if match else ""
            if field_name:
                verbose_field_name = _get_verbose_field_name(field_name)
                message = f"La valeur '{value_given}' n'est pas valide pour le champ '{verbose_field_name}'."
        return (message, code)
