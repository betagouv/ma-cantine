import logging

from django.conf import settings
from django.contrib.auth import get_user_model, tokens, update_session_auth_hash
from django.http import JsonResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from drf_spectacular.utils import extend_schema, extend_schema_view
from oauth2_provider.contrib.rest_framework import TokenHasResourceScope
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response

from api.permissions import IsAuthenticated, IsProfileOwner
from api.serializers import LoggedUserSerializer, PasswordSerializer, UserInfoSerializer
from common.utils import send_mail

logger = logging.getLogger(__name__)


@extend_schema_view(
    get=extend_schema(
        summary="Obtenir des informations sur l'utilisateur identifié.",
        description="Permet d'obtenir des informations sur l'utilisateur.",
        tags=["Utilisateurs"],
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
    permission_classes = [IsAuthenticated, IsProfileOwner]
    required_scopes = ["user"]
    http_method_names = ["patch"]  # disable "put"
    queryset = get_user_model().objects.all()
    serializer_class = LoggedUserSerializer

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
