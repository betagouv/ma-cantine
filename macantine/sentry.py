from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError


def before_send(event, hint):
    """
    Sentry loggs handled exceptions as well as unhandled. We may want to filter
    out some of the exceptions. For instance, PermissionDenied and ValidationErrors
    that occur on the diagnostic import can be safely ignored.
    """

    exception_type, _, _ = hint.get("exc_info")
    module = hint.get("log_record").module

    modules = ["diagnosticimport", "purchaseimport"]
    exceptions = [
        PermissionDenied,
        ValidationError,
        IndexError,
        UnicodeDecodeError,
    ]

    try:
        # Defered loading because at the time of loading this file
        # the app registry is not ready yet.
        # django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.

        from data.models import Sector
        from api.views.diagnosticimport import FileFormatError

        exceptions.append(Sector.DoesNotExist)
        exceptions.append(FileFormatError)
    except Exception:
        pass

    for exc in exceptions:
        if exception_type == exc and module in modules:
            return None

    return event
