import logging

from django.db.models import Count, Min
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_naive, make_aware

from common.utils.commands import MaCantineBaseCommand
from data.models import Canteen, Diagnostic, EventLog, Purchase
from imports.models import ImportType
from data.models.creation_source import CreationSource

logger = logging.getLogger(__name__)

BATCH_SIZE = 1000
DEFAULT_WINDOW_SECONDS = 30
SOURCE_PURCHASE = "purchase"
SOURCE_HISTORY = "history"
SOURCE_CHOICES = [SOURCE_PURCHASE, SOURCE_HISTORY]

# view class name (end of history_change_reason) -> (import type, is the main object a diagnostic, type uncertain)
HISTORY_VIEWS = {
    # current views
    "CanteensCreateImportView": (ImportType.CANTEEN_CREATE, False, False),
    "CanteensUpdateImportView": (ImportType.CANTEEN_UPDATE, False, False),
    "CanteensManagersImportView": (ImportType.CANTEEN_MANAGERS, False, False),
    "DiagnosticsSimpleImportView": (ImportType.DIAGNOSTIC_SIMPLE_SIRET, True, True),  # SIRET or ID
    "DiagnosticsCompleteImportView": (ImportType.DIAGNOSTIC_COMPLETE, True, False),
    # old views
    "CanteensImportView": (ImportType.CANTEEN_ONLY, False, False),
    "ImportCanteensView": (ImportType.CANTEEN_ONLY, False, False),
    "ImportSimpleDiagnosticsView": (ImportType.DIAGNOSTIC_SIMPLE_SIRET, True, False),
    "ImportCompleteDiagnosticsView": (ImportType.DIAGNOSTIC_COMPLETE, True, False),
    "ImportSimpleCentralKitchenView": (ImportType.CC_SIMPLE, True, False),
    "ImportCompleteCentralKitchenView": (ImportType.CC_COMPLETE, True, False),
}


class Command(MaCantineBaseCommand):
    """
    One shot: create an EventLog (category IMPORT, status SUCCESS) for each past successful import
    (before the live EventLog import logging)

    2 sources:
    - purchase: purchase imports. One import = one file = one file digest (Purchase.import_source)
        - user: the purchases creation_user, date: the first purchase creation_date
        - SIRET & ID imports can't be told apart: name is always PURCHASE (data["import_type_uncertain"])
    - history: canteen & diagnostic imports, rebuilt from the Canteen & Diagnostic history
        - imports write history rows with history_change_reason = "Mass CSV import[ - ...]. <ViewClassName>"
          (only on success: failed imports are rolled back)
        - one import = the history rows of the same user & view, without a gap of more than --window-seconds
        - name: the import type of the view (see HISTORY_VIEWS), user: history_user, date: the first row history_date
        - approximate: two imports of the same user & view less than --window-seconds apart are merged,
          history rows removed by the history cleanup (MAX_DAYS_HISTORICAL_RECORDS) are lost

    For both:
    - canteen: if the import concerns a single (still existing) canteen
    - data: count, seconds (always None: no duration), backfilled, source

    Not idempotent: run it only once (each run creates the EventLog again)

    Usage (once per source):
    - python manage.py eventlog_backfill_imports --before 2026-10-20T00:00 --source purchase
    - python manage.py eventlog_backfill_imports --before 2026-10-20T00:00 --source purchase --apply
    - python manage.py eventlog_backfill_imports --before 2026-10-20T00:00 --source history --apply
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--before",
            type=str,
            required=True,
            help="Only imports before this datetime (ISO format): the deployment date of the live EventLog import logging.",
        )
        parser.add_argument(
            "--source",
            type=str,
            choices=SOURCE_CHOICES,
            required=True,
            help="Source of the imports to backfill.",
        )
        parser.add_argument(
            "--window-seconds",
            type=int,
            default=DEFAULT_WINDOW_SECONDS,
            help=f"history source: max gap between 2 history rows of the same import (default: {DEFAULT_WINDOW_SECONDS}).",
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
        source = options["source"]
        apply = options["apply"]
        logger.info(
            f"Start task: eventlog_backfill_imports (before={before.isoformat()}) (source={source}) "
            f"(window_seconds={options['window_seconds']}) (apply={apply})"
        )

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        if source == SOURCE_PURCHASE:
            imports = self._get_purchase_imports(before)
        else:
            imports = self._get_history_imports(before, options["window_seconds"])

        logger.info(f"{len(imports)} imports to backfill")
        for name in sorted({i["name"] for i in imports}):
            logger.info(f"- {name}: {len([i for i in imports if i['name'] == name])} imports")

        if apply:
            existing_canteen_ids = set(
                Canteen.all_objects.filter(id__in={i["canteen_id"] for i in imports if i["canteen_id"]}).values_list(
                    "id", flat=True
                )
            )
            for start in range(0, len(imports), BATCH_SIZE):
                self._backfill_batch(imports[start : start + BATCH_SIZE], existing_canteen_ids)
            logger.info(f"{len(imports)} EventLog created")

    def _get_purchase_imports(self, before):
        purchase_imports = (
            Purchase.all_objects.filter(creation_source=CreationSource.IMPORT, creation_date__lt=before)
            .exclude(import_source__isnull=True)
            .exclude(import_source="")
            .values("import_source")
            .annotate(
                count=Count("id"),
                first_creation_date=Min("creation_date"),
                user_id=Min("creation_user_id"),
                canteen_count=Count("canteen_id", distinct=True),
                canteen_id=Min("canteen_id"),
            )
            .order_by("first_creation_date")
        )
        imports = [
            {
                "name": ImportType.PURCHASE,
                "user_id": purchase_import["user_id"],
                "canteen_id": purchase_import["canteen_id"] if purchase_import["canteen_count"] == 1 else None,
                "date": purchase_import["first_creation_date"],
                "data": self._get_data(
                    source=SOURCE_PURCHASE,
                    count=purchase_import["count"],
                    import_type_uncertain=True,
                    file_digest=purchase_import["import_source"],
                ),
            }
            for purchase_import in purchase_imports.iterator()
        ]
        logger.info(f"purchase: {len(imports)} imports ({sum(i['data']['count'] for i in imports)} purchases)")
        return imports

    def _get_history_imports(self, before, window_seconds):
        rows, unknown_views = self._get_history_rows(before)
        groups = self._group_history_rows(rows, window_seconds)
        imports = []
        for group in groups:
            import_type, is_diagnostic_import, is_import_type_uncertain = HISTORY_VIEWS[group["view"]]
            main_ids = (
                group["diagnostic_ids"] if is_diagnostic_import and group["diagnostic_ids"] else group["canteen_ids"]
            )
            imports.append(
                {
                    "name": import_type,
                    "user_id": group["user_id"],
                    "canteen_id": next(iter(group["canteen_ids"])) if len(group["canteen_ids"]) == 1 else None,
                    "date": group["first_date"],
                    "data": self._get_data(
                        source=SOURCE_HISTORY,
                        count=len(main_ids),
                        import_type_uncertain=is_import_type_uncertain,
                        view=group["view"],
                    ),
                }
            )
        logger.info(f"history: {len(rows)} history rows -> {len(imports)} imports")
        if unknown_views:
            logger.info(f"history: ignored (unknown views): {unknown_views}")
        return imports

    def _get_history_rows(self, before):
        """(user_id, view, history_date, canteen_id, diagnostic_id) for each import history row"""
        rows = []
        unknown_views = {}
        for model, canteen_field, diagnostic_field in [(Canteen, "id", None), (Diagnostic, "canteen_id", "id")]:
            fields = ["history_user_id", "history_change_reason", "history_date", canteen_field]
            if diagnostic_field:
                fields.append(diagnostic_field)
            queryset = model.history.model.objects.filter(
                history_change_reason__startswith="Mass CSV import", history_date__lt=before
            ).values_list(*fields)
            for values in queryset.iterator(chunk_size=BATCH_SIZE):
                user_id, reason, history_date, canteen_id = values[:4]
                view = reason.rsplit(". ", 1)[-1]
                if view not in HISTORY_VIEWS:
                    unknown_views[view] = unknown_views.get(view, 0) + 1
                    continue
                rows.append((user_id, view, history_date, canteen_id, values[4] if diagnostic_field else None))
        return rows, unknown_views

    def _group_history_rows(self, rows, window_seconds):
        groups = []
        rows.sort(key=lambda row: (row[0] or 0, row[1], row[2]))
        current, previous = None, None
        for row in rows:
            user_id, view, history_date, canteen_id, diagnostic_id = row
            is_new_group = (
                previous is None
                or (user_id, view) != previous[:2]
                or (history_date - previous[2]).total_seconds() > window_seconds
            )
            if is_new_group:
                current = {
                    "user_id": user_id,
                    "view": view,
                    "first_date": history_date,
                    "canteen_ids": set(),
                    "diagnostic_ids": set(),
                }
                groups.append(current)
            if canteen_id:
                current["canteen_ids"].add(canteen_id)
            if diagnostic_id:
                current["diagnostic_ids"].add(diagnostic_id)
            previous = row
        return groups

    @staticmethod
    def _get_data(source, count, import_type_uncertain, **extra):
        return {
            "message": None,
            "count": count,
            "seconds": None,
            "backfilled": True,
            "source": source,
            "import_type_uncertain": import_type_uncertain,
            **extra,
        }

    def _backfill_batch(self, imports, existing_canteen_ids):
        event_logs = EventLog.objects.bulk_create(
            [
                EventLog(
                    category=EventLog.Category.IMPORT,
                    name=i["name"],
                    status=EventLog.Status.SUCCESS,
                    user_id=i["user_id"],
                    canteen_id=i["canteen_id"] if i["canteen_id"] in existing_canteen_ids else None,
                    data=i["data"],
                )
                for i in imports
            ]
        )
        # bulk_update skips auto_now_add / auto_now
        for event_log, i in zip(event_logs, imports):
            event_log.creation_date = i["date"]
            event_log.modification_date = i["date"]
        EventLog.objects.bulk_update(event_logs, ["creation_date", "modification_date"])
