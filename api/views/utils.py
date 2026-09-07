import logging

from django.db.models import Model
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.models import Application
from rest_framework.request import Request
from rest_framework.views import APIView
from simple_history.utils import update_change_reason

logger = logging.getLogger(__name__)


def get_oauth_application(request: Request) -> Application | None:
    """Extract OAuth Application object from request if authenticated via token"""
    if isinstance(request.successful_authenticator, OAuth2Authentication):
        if request.auth and hasattr(request.auth, "application"):
            return request.auth.application
    return None


def update_change_reason_with_auth(view: APIView, obj: Model) -> None:
    try:
        update_change_reason(
            obj, f"{view.request.successful_authenticator.__class__.__name__[:100]}"
        )  # The max allowed chars is 100
    except Exception as e:
        logger.warning(f"Unable to set reason change on {view.__class__.__name__} for object ID : {obj.id}: \n{e}")
        update_change_reason(obj, "Unknown")
