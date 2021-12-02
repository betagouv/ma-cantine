from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
import logging

# not importing create_trello_card directly because that breaks patching for tests
import common.utils as utils

logger = logging.getLogger(__name__)


class InquiryView(APIView):
    inquiry_types = {
        "functionalityQuestion": "fonctionnalité",
        "egalim": "loi",
        "bug": "bug",
        "other": "autre",
    }
    # Auto assign members based on question type?

    def post(self, request):
        try:
            inquiry_type = request.data.get("inquiry_type")
            if inquiry_type not in self.inquiry_types:
                inquiry_type = "other"

            email = request.data.get("from")

            title = f"{email} - {self.inquiry_types[inquiry_type]}"
            body = f"Message\n---\n{request.data.get('message')}"
            body += "\nDétails\n---"
            body += f"\nAdresse : {email}"
            for key, value in request.data.get("meta").items():
                body += f"\n{key} : {value}"
            utils.create_trello_card(title, body)

            return JsonResponse({}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Exception ocurred while handling inquiry. Title: {title}, Body:\n{body}")
            logger.exception(e)
            print(e)
            return JsonResponse(
                {"error": "An error has ocurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
