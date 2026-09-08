import json
import re

from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from djangorestframework_camel_case.util import camelize_re, underscore_to_camel


def camelize(data: str | dict | list) -> str | dict | list:
    if isinstance(data, str):
        return re.sub(camelize_re, underscore_to_camel, data)
    camel_case_bytes = CamelCaseJSONRenderer().render(data)
    return json.loads(camel_case_bytes.decode("utf-8"))
