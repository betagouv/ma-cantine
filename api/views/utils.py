import json
from djangorestframework_camel_case.render import CamelCaseJSONRenderer


def camelize(data):
    camel_case_bytes = CamelCaseJSONRenderer().render(data)
    return json.loads(camel_case_bytes.decode("utf-8"))
