import json
import logging

import chardet
from django.conf import settings
from django.core.exceptions import ValidationError
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.views import APIView
from simple_history.utils import update_change_reason

logger = logging.getLogger(__name__)


class CSVImportApiView(APIView):
    def _verify_file_size(self):
        if self.file.size > settings.CSV_IMPORT_MAX_SIZE:
            raise ValidationError("Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo")

    def _verify_file_format(self):
        if self.file.content_type not in ["text/csv", "text/tab-separated-values"]:
            raise ValidationError(
                f"Ce fichier est au format {self.file.content_type}, merci d'exporter votre fichier au format CSV et réessayer."
            )


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


def decode_bytes(bytes_string):
    detection_result = chardet.detect(bytes_string)
    encoding_detected = detection_result["encoding"]
    logger.info(f"Encoding autodetected : {encoding_detected}")
    return (bytes_string.decode(encoding_detected), encoding_detected)
