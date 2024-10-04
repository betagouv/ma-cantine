import json
import logging

import sib_api_v3_sdk
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


class SubscribeNewsletter(APIView):
    def post(self, request):
        try:
            email = request.data.get("email", "")
            if not email:
                raise ValidationError("No email given")
            email = email.strip()
            validate_email(email)

            list_id = settings.NEWSLETTER_SENDINBLUE_LIST_ID
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key["api-key"] = settings.ANYMAIL.get("SENDINBLUE_API_KEY")
            api_instance = sib_api_v3_sdk.ContactsApi(sib_api_v3_sdk.ApiClient(configuration))
            create_contact = sib_api_v3_sdk.CreateContact(email=email)
            create_contact.list_ids = [int(list_id)]
            create_contact.update_enabled = True
            api_instance.create_contact(create_contact)
            return JsonResponse({}, status=status.HTTP_200_OK)
        except sib_api_v3_sdk.rest.ApiException as e:
            contact_exists = json.loads(e.body).get("message") == "Contact already exist"
            if contact_exists:
                logger.warning(f"Newsletter contact already exists: {email}")
                return JsonResponse({}, status=status.HTTP_200_OK)
            logger.exception("SIB API error in newsletter subsription :\n{e}")
            return JsonResponse(
                {"error": "Error calling SendInBlue API"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            logger.warning(f"Invalid email on newsletter subscription: {email}:\n{e}")
            return JsonResponse({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"Error on newsletter subscription:\n{e}")
            return JsonResponse(
                {"error": "An error has ocurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
