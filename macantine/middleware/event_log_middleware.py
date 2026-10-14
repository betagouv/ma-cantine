import logging
import re
import time

from oauth2_provider.models import get_access_token_model

from data.models import EventLog

logger = logging.getLogger(__name__)

LOGGED_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
MESSAGE_MAX_LENGTH = 1000
ROUTE_PARAMETER_REGEX = re.compile(r"<(?:\w+:)?(\w+)>")  # <int:canteen_pk> or <canteen_pk>


class EventLogMiddleware:
    """
    Create an EventLog (category API) for each write request (POST, PUT, PATCH, DELETE)
    on the API made with an OAuth2 token (web app requests are not logged)

    DRF propagates request.user & request.auth to the Django request once the view has authenticated it:
    so they can only be read after the response.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        if request.method in LOGGED_METHODS and request.path.startswith("/api/"):
            self._log(request, response, start_time)
        return response

    def _log(self, request, response, start_time):
        try:
            access_token = getattr(request, "auth", None)
            if not isinstance(access_token, get_access_token_model()):
                return
            is_success = response.status_code < 400
            EventLog.log(
                EventLog.Category.API,
                f"{request.method} {self._get_route(request)}",
                EventLog.Status.SUCCESS if is_success else EventLog.Status.FAILURE,
                user=getattr(request, "user", None),
                api_oauth2_application=access_token.application,
                data={
                    "method": request.method,
                    "path": request.path,
                    "status_code": response.status_code,
                    "seconds": round(time.time() - start_time, 2),
                    "message": None if is_success else self._get_message(response),
                },
            )
        except Exception:
            logger.exception(f"EventLog: could not log API request {request.method} {request.path}")

    @staticmethod
    def _get_route(request):
        """
        The route rather than the path, to group requests by endpoint
        In the OpenAPI format (same as /api/docs/): '^api/v1/canteens/<int:canteen_pk>/diagnostics/<int:pk>'
        -> '/api/v1/canteens/{canteen_pk}/diagnostics/{id}' (drf-spectacular renames pk to id)
        """
        resolver_match = getattr(request, "resolver_match", None)
        if resolver_match and resolver_match.route:
            route = resolver_match.route.lstrip("^").rstrip("$")
            return "/" + ROUTE_PARAMETER_REGEX.sub(EventLogMiddleware._format_route_parameter, route)
        return request.path

    @staticmethod
    def _format_route_parameter(match):
        parameter = match.group(1)
        return "{id}" if parameter == "pk" else "{" + parameter + "}"

    @staticmethod
    def _get_message(response):
        if getattr(response, "streaming", False):
            return None
        return response.content.decode("utf-8", errors="replace")[:MESSAGE_MAX_LENGTH]
