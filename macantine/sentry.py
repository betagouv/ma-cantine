from django.core.exceptions import ValidationError
from rest_framework.exceptions import PermissionDenied


def before_send(event, hint):
    """
    Sentry logs handled exceptions as well as unhandled. We may want to filter
    out some of the exceptions. For instance, PermissionDenied and ValidationErrors
    that occur on the imports can be safely ignored.
    """

    # only logged exceptions can be filtered out. The other events (e.g. sentry_sdk.capture_exception(),
    # captured messages) have no "exc_info" and/or "log_record": unpacking them would raise,
    # and Sentry drops the event when before_send raises
    exc_info = hint.get("exc_info")
    log_record = hint.get("log_record")
    if not exc_info or not log_record:
        return event

    exception_type, _, _ = exc_info
    module = log_record.module

    modules = [
        "canteen_create_import",
        "canteen_update_import",
        "canteen_managers_import",
        "diagnostic_import",
        "purchase_import",
    ]
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

        from data.models import SectorM2M

        exceptions.append(SectorM2M.DoesNotExist)
    except Exception:
        pass

    for exc in exceptions:
        if exception_type == exc and module in modules:
            return None

    return event
