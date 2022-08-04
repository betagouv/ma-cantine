import logging
import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework.views import APIView
from rest_framework import status
import sib_api_v3_sdk

logger = logging.getLogger(__name__)


class PipedriveException(Exception):
    pass


class PipedriveUtils:

    base_url = "https://companydomain.pipedrive.com/api/v1"
    api_token = settings.PIPEDRIVE_API_TOKEN

    @classmethod
    def search_person(cls, email):
        url = f"{cls.base_url}/persons/search?term={email}&api_token={cls.api_token}"
        return PipedriveUtils._verify_response(requests.get(url))

    @classmethod
    def create_person(cls, email, phone_number, name):
        url = f"{cls.base_url}/persons?api_token={cls.api_token}"
        payload = {
            "email": [email],
            "name": name or "",
            "phone": phone_number,
        }
        return PipedriveUtils._verify_response(requests.post(url, payload))

    @classmethod
    def create_card(cls, title, person_id, city):
        url = f"{cls.base_url}/deals?api_token={cls.api_token}"
        payload = {"title": title, "person_id": person_id, "a3d1bd0770105926c096f2c49d3331dc1bc4ef74": city}

        return PipedriveUtils._verify_response(requests.post(url, json=payload))

    @classmethod
    def create_note(cls, content, deal_id):
        url = f"{cls.base_url}/notes?api_token={cls.api_token}"
        payload = {"content": content, "deal_id": deal_id}

        return PipedriveUtils._verify_response(requests.post(url, json=payload))

    @staticmethod
    def _verify_response(pipedrive_response):
        response = pipedrive_response.json()
        if not response.get("success"):
            raise PipedriveException(f"Pipedrive API fail : {pipedrive_response}")
        return response


class SubscribeBetaTester(APIView):
    def post(self, request):
        try:
            data = request.data
            email = data["email"]
            phone = data.get("phone")
            name = data.get("name")
            city = data.get("city")
            message = data.get("message")
            title = "Nouveau beta tester"

            search_results = PipedriveUtils.search_person(email)

            search_results_data = search_results.get("data")
            search_items = search_results_data.get("items") if search_results_data else []

            if search_items:
                person_id = search_items[0]["item"]["id"]
            else:
                created_person = PipedriveUtils.create_person(email, phone, name)
                person_id = created_person["data"]["id"]

            card_creation = PipedriveUtils.create_card(title, person_id, city)

            if message:
                card_id = card_creation["data"]["id"]
                PipedriveUtils.create_note(f"Note de l'utilisateur :\n{message}", card_id)

            return JsonResponse({}, status=status.HTTP_201_CREATED)

        except PipedriveException as e:
            logger.exception(f"Pipedrive API error on request by {name or ''} {email}: {message}:\n{e}")
            return JsonResponse({}, status=status.HTTP_502_BAD_GATEWAY)

        except Exception as e:
            logger.exception(f"Error on beta-tester subscription:\n{e}")
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)


class SubscribeNewsletter(APIView):
    def post(self, request):
        try:
            email = request.data.get("email", "").strip()
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
                logger.warning(f"Beta-tester already exists: {email}")
                return JsonResponse({}, status=status.HTTP_200_OK)
            logger.exception("SIB API error in beta-tester subsription :\n{e}")
            return JsonResponse(
                {"error": "Error calling SendInBlue API"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            logger.warning(f"Invalid email on beta-tester subscription: {email}:\n{e}")
            return JsonResponse({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"Error on newsletter subscription:\n{e}")
            return JsonResponse(
                {"error": "An error has ocurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
