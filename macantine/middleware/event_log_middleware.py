import logging
import time

from oauth2_provider.models import get_access_token_model

from data.models import EventLog

logger = logging.getLogger(__name__)

LOGGED_METHODS = {"POST", "PUT", "PATCH", "DELETE"}
MESSAGE_MAX_LENGTH = 1000


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
        """The route (e.g. 'api/v1/canteens/<int:pk>') rather than the path, to group requests by endpoint"""
        resolver_match = getattr(request, "resolver_match", None)
        if resolver_match and resolver_match.route:
            return resolver_match.route.lstrip("^")
        return request.path

    @staticmethod
    def _get_message(response):
        if getattr(response, "streaming", False):
            return None
        return response.content.decode("utf-8", errors="replace")[:MESSAGE_MAX_LENGTH]
