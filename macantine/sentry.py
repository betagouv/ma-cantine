from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from api.views.diagnosticimport import FileFormatError


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
        FileFormatError,
    ]

    try:
        from data.models import Sector

        exceptions.append(Sector.DoesNotExist)
    except Exception:
        pass

    for exc in exceptions:
        if exception_type == exc and module in modules:
            return None

    return event
