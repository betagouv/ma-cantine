from data.models.diagnostic import Diagnostic
import json
from django.contrib.auth import get_user_model, update_session_auth_hash, tokens
from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template import loader
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist, ValidationError, BadRequest
from django.db.utils import IntegrityError
from django.core.validators import validate_email
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView
from rest_framework.generics import UpdateAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from api.serializers import LoggedUserSerializer, DiagnosticSerializer, SectorSerializer
from api.serializers import (
    PublicCanteenSerializer,
    FullCanteenSerializer,
    BlogPostSerializer,
    PasswordSerializer,
    ManagingTeamSerializer
)
from data.models import Canteen, BlogPost, Sector, ManagerInvitation
from api.permissions import IsProfileOwner, IsCanteenManager, CanEditDiagnostic
import sib_api_v3_sdk
from djangorestframework_camel_case.render import CamelCaseJSONRenderer


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
        new_email = serializer.validated_data.get('email', previous_email)

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
            message=loader.render_to_string(text_template, context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            html_message=loader.render_to_string(html_template, context),
            recipient_list=[new_email],
            fail_silently=False,
        )




class PublishedCanteensView(ListAPIView):
    model = Canteen
    serializer_class = PublicCanteenSerializer
    queryset = Canteen.objects.filter(data_is_public=True)


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
        previous_publication_status = serializer.instance.data_is_public
        new_publication_status = serializer.validated_data.get("data_is_public", False)

        if not previous_publication_status and new_publication_status:
            protocol = "https" if settings.SECURE else "http"
            cantine = serializer.instance
            admin_url = "{}://{}/admin/data/canteen/{}/change/".format(
                protocol, settings.HOSTNAME, cantine.id
            )
            canteens_url = "{}://{}/nos-cantines/".format(protocol, settings.HOSTNAME)

            send_mail(
                "Cantine publiée sur ma cantine",
                "La cantine « {} » vient d'être publiée.\nAdmin : {}\nNos cantines : {}".format(
                    cantine.name, admin_url, canteens_url
                ),
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


class BlogPostsView(ListAPIView):
    model = BlogPost
    serializer_class = BlogPostSerializer
    queryset = BlogPost.objects.filter(published=True)


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
                {"error": "An error has ocurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
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

def _respond_with_team(canteen):
    data = ManagingTeamSerializer(canteen).data
    camel_case_bytes = CamelCaseJSONRenderer().render(data)
    json_data = json.loads(camel_case_bytes.decode('utf-8'))
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
            message=render_to_string(f"{template}.html", context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            html_message=render_to_string(f"{template}.txt", context),
            recipient_list=[manager_invitation.email],
            fail_silently=False,
        )
    except Exception:
        raise Exception("Error occurred : the mail could not be sent.")
