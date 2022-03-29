from django.http import JsonResponse
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
import logging

# not importing create_trello_card directly because that breaks patching for tests
import common.utils as utils

logger = logging.getLogger(__name__)


class InquiryView(APIView):
    def post(self, request):
        try:
            email = request.data.get("from")
            name = request.data.get("name")
            message = request.data.get("message")
            inquiry_type = request.data.get("inquiry_type", "autre")
            meta = request.data.get("meta") or {}

            InquiryView._raise_for_mandatory_fields(email, message)

            title = f"{email} - {inquiry_type}"

            env = getattr(settings, "ENVIRONMENT", "")
            if env == "demo" or env == "staging":
                title = f"({env.upper()}) {title}"

            body = f"Nom/Prénom\n---\n{name or 'Non renseigné'}"
            body += f"\nMessage\n---\n{message}"
            body += "\nDétails\n---"
            body += f"\nAdresse : {email}"
            for key, value in meta.items():
                body += f"\n{key} : {value}"
            utils.create_trello_card(settings.TRELLO_LIST_ID_CONTACT, title, body)

            return JsonResponse({}, status=status.HTTP_200_OK)
        except ValidationError as e:
            logger.error("Missing field from inquiry view")
            logger.exception(e)
            raise e
        except Exception as e:
            logger.error(f"Exception ocurred while handling inquiry. Title: {title}, Body:\n{body}")
            logger.exception(e)
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
