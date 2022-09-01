from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponseRedirect


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        setting_value = getattr(settings, "ENFORCE_HOST", None)

        if setting_value is None:
            raise MiddlewareNotUsed()

        self.redirect_to = setting_value

    def __call__(self, request):
        host = request.get_host().split(":")[0]
        port = request.get_port()

        if host in self.redirect_to:
            return self.get_response(request)

        new_url = "{}://{}{}{}".format(
            "https" if request.is_secure() else "http",
            self.redirect_to,
            f":{port}" if port and port == "8000" else "",
            request.get_full_path(),
        )

        return HttpResponseRedirect(new_url)
