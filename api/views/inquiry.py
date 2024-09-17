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
            message = request.data.get("message")
            inquiry_type = request.data.get("inquiry_type", "autre")
            meta = request.data.get("meta") or {}

            InquiryView._raise_for_mandatory_fields(email, message)

            title = f"Demande de support de {email} - {inquiry_type}"

            body = f"Nom/Prénom\n---\n{name or 'Non renseigné'}"
            body += f"\nMessage\n---\n{message}"
            body += "\nDétails\n---"
            body += f"\nAdresse : {email}"
            for key, value in meta.items():
                body += f"\n{key} : {value}"

            utils.send_mail(message=body, subject=title, to=[settings.CONTACT_EMAIL], reply_to=[email])

            return JsonResponse({}, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.exception("Missing field from inquiry view:\n{e}")
            raise e
        except Exception as e:
            logger.exception(f"Exception ocurred while handling inquiry. Title: {title}, Body:\n{body}:\n{e}")
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
