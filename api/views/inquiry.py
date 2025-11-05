import logging

from django.conf import settings
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

import common.utils as utils

logger = logging.getLogger(__name__)


class InquiryView(APIView):
    def post(self, request):
        try:
            email = request.data.get("from", "").strip()
            name = request.data.get("name")
            username = request.data.get("username")
            message = request.data.get("message")
            siret_or_siren = request.data.get("siret_or_siren")
            inquiry_type = request.data.get("inquiry_type", "autre")
            meta = request.data.get("meta") or {}

            InquiryView._raise_for_mandatory_fields(email, message)

            title = f"Demande de support de {email} - {inquiry_type}"
            context = {
                "name": name or "Non renseigné",
                "username": username or "Non renseigné",
                "siret_or_siren": siret_or_siren or "Non renseigné",
                "message": message,
                "details": meta.items(),
            }

            utils.send_mail(
                template="email_contact", context=context, subject=title, to=[settings.CONTACT_EMAIL], reply_to=[email]
            )

            return JsonResponse({}, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.exception("Missing field from inquiry view:\n{e}")
            raise e
        except Exception as e:
            logger.exception(f"Exception ocurred while handling inquiry. Title: {title}, Context:\n{context}:\n{e}")
            return JsonResponse(
                {"error": "An error has ocurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @staticmethod
    def _raise_for_mandatory_fields(email, message):
        missing_mandatory_fields = {}
        if not email:
            missing_mandatory_fields["from"] = "Merci d'indiquer une adresse email"
        if not message:
            missing_mandatory_fields["message"] = "Message manquant dans la requête"
        if missing_mandatory_fields:
            raise ValidationError(missing_mandatory_fields)
