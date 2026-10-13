import logging

from django.db.models import Count, Min
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_naive, make_aware

from common.utils.commands import MaCantineBaseCommand
from data.models import EventLog, ImportType, Purchase
from data.models.creation_source import CreationSource

logger = logging.getLogger(__name__)

BATCH_SIZE = 1000


class Command(MaCantineBaseCommand):
    """
    Create an EventLog (category IMPORT, status SUCCESS) for each past successful purchase import

    One import = one file = one file digest (Purchase.import_source)
    - user: the purchases creation_user
    - creation_date: the first purchase creation_date
    - data: count (number of purchases), backfilled & file_digest (to skip the imports already backfilled)

    Limits:
    - SIRET & ID imports can't be told apart: name is always PURCHASE (data["import_type_uncertain"] = True)
    - no duration (data["seconds"] = None)
    - purchases hard-deleted since are not counted

    Usage:
    - python manage.py eventlog_backfill_purchase_imports --before 2026-10-20T00:00
    - python manage.py eventlog_backfill_purchase_imports --before 2026-10-20T00:00 --apply
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--before",
            type=str,
            required=True,
            help="Only imports before this datetime (ISO format): the deployment date of the live EventLog import logging.",
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
        logger.info(f"Start task: eventlog_backfill_purchase_imports (before={before.isoformat()}) (apply={apply})")

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        already_backfilled_digests = set(
            EventLog.objects.filter(category=EventLog.Category.IMPORT, data__has_key="file_digest").values_list(
                "data__file_digest", flat=True
            )
        )

        imports = (
            Purchase.all_objects.filter(creation_source=CreationSource.IMPORT, creation_date__lt=before)
            .exclude(import_source__isnull=True)
            .exclude(import_source="")
            .values("import_source")
            .annotate(count=Count("id"), first_creation_date=Min("creation_date"), user_id=Min("creation_user_id"))
            .order_by("first_creation_date")
        )

        imports_to_backfill = [i for i in imports.iterator() if i["import_source"] not in already_backfilled_digests]
        purchase_count = sum(i["count"] for i in imports_to_backfill)
        logger.info(
            f"{len(imports_to_backfill)} purchase imports to backfill ({purchase_count} purchases), "
            f"{len(already_backfilled_digests)} already backfilled"
        )

        if apply:
            for start in range(0, len(imports_to_backfill), BATCH_SIZE):
                self._backfill_batch(imports_to_backfill[start : start + BATCH_SIZE])
            logger.info(f"{len(imports_to_backfill)} EventLog created")

    def _backfill_batch(self, imports):
        event_logs = EventLog.objects.bulk_create(
            [
                EventLog(
                    category=EventLog.Category.IMPORT,
                    name=ImportType.PURCHASE,
                    status=EventLog.Status.SUCCESS,
                    user_id=purchase_import["user_id"],
                    data={
                        "message": None,
                        "count": purchase_import["count"],
                        "seconds": None,
                        "backfilled": True,
                        "file_digest": purchase_import["import_source"],
                        "import_type_uncertain": True,
                    },
                )
                for purchase_import in imports
            ]
        )
        # bulk_update skips auto_now_add / auto_now
        for event_log, purchase_import in zip(event_logs, imports):
            event_log.creation_date = purchase_import["first_creation_date"]
            event_log.modification_date = purchase_import["first_creation_date"]
        EventLog.objects.bulk_update(event_logs, ["creation_date", "modification_date"])
