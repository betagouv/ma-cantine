import json
import logging

import sib_api_v3_sdk
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from macantine.brevo import create_newsletter_contact

logger = logging.getLogger(__name__)


class SubscribeNewsletter(APIView):
    def post(self, request):
        try:
            email = request.data.get("email", "")
            if not email:
                raise ValidationError("No email given")
            email = email.strip()
            validate_email(email)
            create_newsletter_contact(email)
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
