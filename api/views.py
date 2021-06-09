from data.models.diagnostic import Diagnostic
import json
from django.contrib.auth import get_user_model
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import validate_email
from rest_framework.generics import RetrieveAPIView, ListAPIView, ListCreateAPIView
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied
from api.serializers import LoggedUserSerializer, DiagnosticSerializer, SectorSerializer
from api.serializers import (
    PublicCanteenSerializer,
    FullCanteenSerializer,
    BlogPostSerializer,
)
from data.models import Canteen, BlogPost, Sector
from api.permissions import IsProfileOwner, IsCanteenManager, CanEditDiagnostic
import sib_api_v3_sdk


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


class UpdateUserCanteenView(UpdateAPIView):
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
                "Nouveau Béta-testeur ma canteen",
                render_to_string("subscription-beta-tester.txt", context),
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                html_message=render_to_string("subscription-beta-tester.html", context),
            )
            return JsonResponse({}, status=status.HTTP_201_CREATED)
        except Exception as e:
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
                {"error": "An error has ocurred"}, status=status.HTTP_400_BAD_REQUEST
            )
