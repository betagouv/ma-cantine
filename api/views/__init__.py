from .user import LoggedUserView, UpdateUserView, ChangePasswordView  # noqa: F401
from .canteen import (  # noqa: F401
    PublishedCanteensView,
    PublishedCanteenSingleView,
    UserCanteensView,
    RetrieveUpdateUserCanteenView,
    AddManagerView,
    RemoveManagerView,
    SendCanteenEmailView,
    PublishCanteenView,
    UnpublishCanteenView,
    SendCanteenNotFoundEmail,
    UserCanteenPreviews,
)
from .diagnostic import (  # noqa: F401
    DiagnosticCreateView,
    DiagnosticUpdateView,
    ImportDiagnosticsView,
)
from .sector import SectorListView  # noqa: F401
from .blog import BlogPostsView, BlogPostView  # noqa: F401
from .subscription import SubscribeBetaTester, SubscribeNewsletter  # noqa: F401
from .teledeclaration import (  # noqa: F401
    TeledeclarationCreateView,
    TeledeclarationCancelView,
    TeledeclarationPdfView,
)
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
                return JsonResponse({"error": "Invalid inquiry type"}, status=status.HTTP_400_BAD_REQUEST)

            email = request.data.get("from")

            title = f"{email} - {self.inquiry_types[inquiry_type]}"
            body = f"Message\n---\n{request.data.get('message')}"
            body += "\nDétailles\n---"
            body += f"\nAdresse : {email}"
            for key, value in request.data.get("meta").items():
                body += f"\n{key} : {value}"
            utils.create_trello_card(title, body)

            return JsonResponse({}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Exception ocurred while handling inquiry")
            logger.exception(e)
            print(e)
            return JsonResponse(
                {"error": "An error has ocurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
