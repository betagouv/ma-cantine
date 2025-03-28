import json
import logging

from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from simple_history.utils import update_change_reason

logger = logging.getLogger(__name__)


def camelize(data):
    camel_case_bytes = CamelCaseJSONRenderer().render(data)
    return json.loads(camel_case_bytes.decode("utf-8"))


def update_change_reason_with_auth(view, object):
    try:
        update_change_reason(
            object, f"{view.request.successful_authenticator.__class__.__name__[:100]}"
        )  # The max allowed chars is 100
    except Exception as e:
        logger.warning(f"Unable to set reason change on {view.__class__.__name__} for object ID : {object.id}: \n{e}")
        update_change_reason(object, "Unknown")
