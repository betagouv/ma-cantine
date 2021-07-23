from data.models.diagnostic import Diagnostic
import json
from django.contrib.auth import get_user_model, update_session_auth_hash, tokens
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist, ValidationError, BadRequest
from django.db.utils import IntegrityError
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
from .utils import normalise_siret


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
    camel_case_bytes = CamelCaseJSONRenderer().render(data)
    json_data = json.loads(camel_case_bytes.decode("utf-8"))
    return JsonResponse(json_data, status=status.HTTP_200_OK)


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
            }
            send_mail(
                subject=f"Un message pour {canteen.name}",
                message=render_to_string(f"{template}.html", context),
                from_email=settings.DEFAULT_FROM_EMAIL,
                html_message=render_to_string(f"{template}.txt", context),
                recipient_list=[user.email for user in canteen.managers.all()],
                fail_silently=False,
            )
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


class ImportDiagnosticsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        filestring = request.data["file"].read().decode("utf-8")
        csvreader = csv.reader(filestring.splitlines())
        created = []
        errors = []
        for row_number, row in enumerate(csvreader, start=1):
            try:
                siret = normalise_siret(row[0])
                with transaction.atomic():
                    try:
                        canteen = Canteen.objects.get(siret=siret)
                    except ObjectDoesNotExist:
                        canteen = Canteen.objects.create()
                        canteen.managers.add(self.request.user)
                        canteen.siret = siret
                        # TODO: fetch information from API
                        # call API from utils
                        # Fields to fill : name, city, city_insee_code, department, postal_code
                        # Corresponding fields from API : unite_legal.denomination, libelle_commune, code_commune, departement, code_postal
                        # Look out for 429 response from API - need to pause to wait for next second if get it
                        canteen.name = row[1]
                        # TODO: add canteen field: parent siret row[2]
                        canteen.meal_count = row[3]
                        # TODO: sectors row[5]
                        canteen.production_type = row[6]
                        canteen.management_type = row[7]
                        canteen.save()  # diagnostic save might fail, still save canteen?

                    diagnostic = Diagnostic.objects.create(canteen_id=canteen.id)
                    year = row[7]
                    diagnostic.year = year
                    diagnostic.value_total_ht = row[8]
                    diagnostic.value_bio_ht = row[9]
                    diagnostic.value_sustainable_ht = row[10]
                    diagnostic.value_fair_trade_ht = row[11]
                    diagnostic.save()
                    created.append({"siret": siret, "year": year})
            except Exception as e:
                errors.append({"row": row_number, "status": 400, "message": str(e)})
        # TODO: response will probably take too long to return depending on sizes of files
        return JsonResponse(
            {"created": created, "errors": errors}, status=status.HTTP_200_OK
        )
