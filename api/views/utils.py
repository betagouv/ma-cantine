import json
import logging

from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from simple_history.utils import update_change_reason

logger = logging.getLogger(__name__)


def camelize(data):
    camel_case_bytes = CamelCaseJSONRenderer().render(data)
    return json.loads(camel_case_bytes.decode("utf-8"))


def get_oauth_application(request):
    """Extract OAuth Application object from request if authenticated via token"""
    if isinstance(request.successful_authenticator, OAuth2Authentication):
        if request.auth and hasattr(request.auth, "application"):
            return request.auth.application
    return None


def update_change_reason_with_auth(view, object):
    try:
        update_change_reason(
            object, f"{view.request.successful_authenticator.__class__.__name__[:100]}"
        )  # The max allowed chars is 100
    except Exception as e:
        logger.warning(f"Unable to set reason change on {view.__class__.__name__} for object ID : {object.id}: \n{e}")
        update_change_reason(object, "Unknown")
