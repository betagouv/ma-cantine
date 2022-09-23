import logging
import string
import re
import random
import unicodedata
from django.contrib.auth import get_user_model, tokens, update_session_auth_hash
from django.conf import settings
from django.http import JsonResponse
from common.utils import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from oauth2_provider.contrib.rest_framework import TokenHasResourceScope
from api.serializers import LoggedUserSerializer, PasswordSerializer, UserInfoSerializer
from api.permissions import IsProfileOwner, IsAuthenticated

logger = logging.getLogger(__name__)


@extend_schema_view(
    get=extend_schema(
        summary="Informations sur l'utilisateur identifié.",
        description="Permet d'obtenir des informations sur l'utilisateur et son état dans notre plateforme.",
    ),
)
class UserInfoView(RetrieveAPIView):
    include_in_documentation = True
    model = get_user_model()
    serializer_class = UserInfoSerializer
    queryset = get_user_model().objects.all()
    required_scopes = ["user"]

    def get(self, request, *args, **kwargs):
        if request.auth:
            if TokenHasResourceScope().has_permission(self.request, self):
                return super().get(request, *args, **kwargs)
            raise PermissionDenied()

        elif IsAuthenticated().has_permission(self.request, self):
            return super().get(request, *args, **kwargs)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        return self.request.user


class LoggedUserView(RetrieveAPIView):
    model = get_user_model()
    serializer_class = LoggedUserSerializer
    queryset = get_user_model().objects.all()

    def get(self, request, *args, **kwargs):
        if IsAuthenticated().has_permission(self.request, self):
            return super().get(request, *args, **kwargs)
        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def get_object(self):
        return self.request.user


class UpdateUserView(UpdateAPIView):
    model = get_user_model()
    serializer_class = LoggedUserSerializer
    permission_classes = [IsAuthenticated, IsProfileOwner]
    required_scopes = ["user"]
    queryset = get_user_model().objects.all()

    def put(self, request, *args, **kwargs):
        return JsonResponse({"error": "Only PATCH request supported in this resource"}, status=405)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        previous_email = serializer.instance.email
        new_email = serializer.validated_data.get("email", previous_email)

        update = super().perform_update(serializer)

        if previous_email != new_email:
            self.unconfirm_email(serializer.instance)
            self.send_confirmation_email(new_email, serializer.instance)
            logger.info(f"Email changed for {self.request.user.id} : {new_email}")

        return update

    def unconfirm_email(self, user):
        user.email_confirmed = False
        user.save()

    def send_confirmation_email(self, new_email, user):
        token = tokens.default_token_generator.make_token(user)
        context = {
            "token": token,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "protocol": settings.PROTOCOL,
            "domain": settings.HOSTNAME,
        }
        send_mail(
            subject="Confirmation de votre changement d'adresse email - ma cantine",
            template="auth/account_activate_email",
            context=context,
            to=[new_email],
        )


class ChangePasswordView(UpdateAPIView):
    serializer_class = PasswordSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        update_session_auth_hash(request, request.user)  # After a password change Django logs the user out
        return JsonResponse({}, status=status.HTTP_200_OK)


class UsernameSuggestionView(APIView):
    class RetryLimitException(Exception):
        pass

    def post(self, request):
        try:
            email = request.data.get("email", "").strip()
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            if first_name and last_name:
                full_name = UsernameSuggestionView._clean_special_chars(f"{first_name.strip()}_{last_name.strip()}")
                suggested = UsernameSuggestionView._generate_username_with_base(full_name)
            elif email:
                email_username = UsernameSuggestionView._clean_special_chars(email.split("@")[0])
                suggested = UsernameSuggestionView._generate_username_with_base(email_username)
            else:
                return JsonResponse({"detail": "Missing info"}, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse({"suggestion": suggested}, status=status.HTTP_200_OK)
        except UsernameSuggestionView.RetryLimitException as e:
            logger.exception(
                f"Unable to generate a username suggestion for first name: {first_name}, last name: {last_name}, email: {email}. Retry limit exceeded.\n{e}"
            )
        except Exception as e:
            logger.exception(f"Unable to generate username suggestion. Unexpected error:\n{e}")

    @staticmethod
    def _generate_username_with_base(username_suggestion, attempt=0):
        limit_retries = 10
        if attempt >= limit_retries:
            raise UsernameSuggestionView.RetryLimitException("Retry limit reached")

        if UsernameSuggestionView._is_unique(username_suggestion):
            return username_suggestion
        new_suggestion = f"{username_suggestion}_{str(random.sample(range(999), 1)[0])}"
        return UsernameSuggestionView._generate_username_with_base(new_suggestion, attempt + 1)

    @staticmethod
    def _is_unique(username):
        try:
            get_user_model().objects.get(username=username)
            return False
        except get_user_model().DoesNotExist:
            return True

    @staticmethod
    def _clean_special_chars(username):
        chars = re.escape(string.punctuation).replace("_", "").replace("-", "")
        normalized_username = unicodedata.normalize("NFKD", username)
        unaccented_username = normalized_username.encode("ASCII", "ignore").decode("utf-8")
        return re.sub(r"[" + chars + "]", "", unaccented_username.strip().lower().replace(" ", "-"))
