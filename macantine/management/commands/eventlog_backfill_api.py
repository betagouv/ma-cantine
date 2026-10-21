import logging

from django.db.models import Q
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_naive, make_aware

from common.utils.commands import MaCantineBaseCommand
from data.models import Canteen, Diagnostic, EventLog, Purchase, WasteMeasurement
from data.models.creation_source import CreationSource

logger = logging.getLogger(__name__)

BATCH_SIZE = 1000

# creations: POST, from creation_source = API
# route in the OpenAPI format (as in /api/docs/), and the name of the canteen id field
CREATION_ROUTES = {
    Canteen: ("/api/v1/canteens/", "id"),
    Diagnostic: ("/api/v1/canteens/{canteen_pk}/diagnostics/", "canteen_id"),
    Purchase: ("/api/v1/canteens/{canteen_pk}/purchases/", "canteen_id"),
    WasteMeasurement: ("/api/v1/canteens/{canteen_pk}/wasteMeasurements/", "canteen_id"),
}
# Purchase & WasteMeasurement: creation_source = API alone is not a proof of an API request
# (the API views use API by default when the client does not send a creation_source: web creations while the frontend
# did not send it, or while creation_source was read-only in the PurchaseSerializer)
# but the OAuth2 application is always stored on API creations (since OAuth2 access to purchases was opened)
CREATIONS_REQUIRING_APPLICATION = {Purchase, WasteMeasurement}
# updates: PATCH (the only update method in /api/docs/), from the history ("~" rows)
# the API views write "OAuth2Authentication" as history_change_reason (update_change_reason_with_auth)
UPDATE_ROUTES = {
    Canteen: ("/api/v1/canteens/{id}", "id"),
    Diagnostic: ("/api/v1/canteens/{canteen_pk}/diagnostics/{id}", "canteen_id"),
    WasteMeasurement: ("/api/v1/canteens/{canteen_pk}/wasteMeasurements/{id}", "canteen_id"),
}


class Command(MaCantineBaseCommand):
    """
    One shot: create an EventLog (category API, status SUCCESS) for each past OAuth2 API write request
    (before the live EventLog API logging), one EventLog per request

    Reuses what is in the DB (see the *_fill_creation_user_and_source commands, to run before):
    - creations (POST): objects with creation_source = API (see CREATION_ROUTES)
        - user: creation_user, application: creation_source_api_oauth2_application, date: creation_date
        - Purchase & WasteMeasurement: only with a creation_source_api_oauth2_application (see CREATIONS_REQUIRING_APPLICATION)
    - updates (PATCH): history "~" rows with history_change_reason = "OAuth2Authentication"
      or history_source = API (see UPDATE_ROUTES)
        - user: history_user, application: history_source_api_oauth2_application (only since its creation),
          date: history_date

    - canteen: the canteen of the object (if it still exists)
    - data: same keys as the live EventLog (method, path, status_code, seconds = None, message = None)
      + backfilled & source ("creation" or "history")

    Lost: failed requests, deletions, updates of the models without history (Purchase),
    Purchase & WasteMeasurement creations without a known application

    Not idempotent: run it only once (each run creates the EventLog again)

    Usage:
    - python manage.py eventlog_backfill_api --before 2026-10-20T00:00
    - python manage.py eventlog_backfill_api --before 2026-10-20T00:00 --apply
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--before",
            type=str,
            required=True,
            help="Only requests before this datetime (ISO format): the deployment date of the live EventLog API logging.",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="To apply changes, otherwise just show what would be done (dry run).",
            default=False,
        )

    def handle(self, *args, **options):
        before = parse_datetime(options["before"])
        if before is None:
            raise ValueError(f"Invalid --before datetime: {options['before']}")
        if is_naive(before):
            before = make_aware(before)
        apply = options["apply"]
        logger.info(f"Start task: eventlog_backfill_api (before={before.isoformat()}) (apply={apply})")

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        events = self._get_creation_events(before) + self._get_update_events(before)

        with_application = len([e for e in events if e["application_id"]])
        logger.info(f"{len(events)} API requests to backfill, {with_application} with an application")
        for name in sorted({e["name"] for e in events}):
            logger.info(f"- {name}: {len([e for e in events if e['name'] == name])}")

        if apply:
            existing_canteen_ids = set(
                Canteen.all_objects.filter(id__in={e["canteen_id"] for e in events if e["canteen_id"]}).values_list(
                    "id", flat=True
                )
            )
            for start in range(0, len(events), BATCH_SIZE):
                self._backfill_batch(events[start : start + BATCH_SIZE], existing_canteen_ids)
            logger.info(f"{len(events)} EventLog created")

    def _get_creation_events(self, before):
        events = []
        for model, (route, canteen_field) in CREATION_ROUTES.items():
            manager = getattr(model, "all_objects", model.objects)  # with the soft-deleted objects
            queryset = manager.filter(creation_source=CreationSource.API, creation_date__lt=before)
            if model in CREATIONS_REQUIRING_APPLICATION:
                queryset = queryset.filter(creation_source_api_oauth2_application__isnull=False)
            queryset = queryset.values_list(
                "creation_user_id", "creation_source_api_oauth2_application_id", "creation_date", "id", canteen_field
            )
            for user_id, application_id, date, object_id, canteen_id in queryset.iterator(chunk_size=BATCH_SIZE):
                events.append(
                    self._get_event(
                        "POST", route, 201, user_id, application_id, date, object_id, canteen_id, source="creation"
                    )
                )
        return events

    def _get_update_events(self, before):
        events = []
        for model, (route, canteen_field) in UPDATE_ROUTES.items():
            queryset = model.history.model.objects.filter(
                Q(history_change_reason="OAuth2Authentication") | Q(history_source=CreationSource.API),
                history_type="~",
                history_date__lt=before,
            ).values_list(
                "history_user_id", "history_source_api_oauth2_application_id", "history_date", "id", canteen_field
            )
            for user_id, application_id, date, object_id, canteen_id in queryset.iterator(chunk_size=BATCH_SIZE):
                events.append(
                    self._get_event(
                        "PATCH", route, 200, user_id, application_id, date, object_id, canteen_id, source="history"
                    )
                )
        return events

    @staticmethod
    def _get_event(method, route, status_code, user_id, application_id, date, object_id, canteen_id, source):
        return {
            "name": f"{method} {route}",
            "user_id": user_id,
            "application_id": application_id,
            "canteen_id": canteen_id,
            "date": date,
            "data": {
                "method": method,
                "path": route.format(id=object_id, canteen_pk=canteen_id),
                "status_code": status_code,
                "seconds": None,
                "message": None,
                "backfilled": True,
                "source": source,
            },
        }

    def _backfill_batch(self, events, existing_canteen_ids):
        event_logs = EventLog.objects.bulk_create(
            [
                EventLog(
                    category=EventLog.Category.API,
                    name=e["name"],
                    status=EventLog.Status.SUCCESS,
                    user_id=e["user_id"],
                    api_oauth2_application_id=e["application_id"],
                    canteen_id=e["canteen_id"] if e["canteen_id"] in existing_canteen_ids else None,
                    data=e["data"],
                )
                for e in events
            ]
        )
        # bulk_update skips auto_now_add / auto_now
        for event_log, e in zip(event_logs, events):
            event_log.creation_date = e["date"]
            event_log.modification_date = e["date"]
        EventLog.objects.bulk_update(event_logs, ["creation_date", "modification_date"])
