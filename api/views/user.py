import logging
from django.contrib.auth import get_user_model, tokens, update_session_auth_hash
from django.conf import settings
from django.http import JsonResponse
from common.utils import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import UpdateAPIView
from rest_framework import permissions, status
from api.serializers import LoggedUserSerializer, PasswordSerializer
from api.permissions import IsProfileOwner

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
            "protocol": "https" if settings.SECURE_SSL_REDIRECT else "http",
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
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        update_session_auth_hash(request, request.user)  # After a password change Django logs the user out
        return JsonResponse({}, status=status.HTTP_200_OK)
