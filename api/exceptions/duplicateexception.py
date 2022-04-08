from rest_framework import status
from rest_framework.exceptions import APIException


class DuplicateException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "La resource que vous souhaitez créer existe déjà"

    def __init__(
        self,
        detail=None,
        code=None,
        additional_data=None,
    ):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code
        if isinstance(additional_data, dict):
            detail = {**{"detail": detail}, **additional_data}
        self.detail = detail
