import logging
from collections import Counter

from common.utils.commands import MaCantineBaseCommand
from common.utils.fill_creation import (
    fill_creation_user,
    get_creation_source_from_first_version,
    get_first_versions,
    update_objects,
)
from data.models import WasteMeasurement
from data.utils import has_charfield_missing_query

logger = logging.getLogger(__name__)


class Command(MaCantineBaseCommand):
    """
    Usage:
    - python manage.py wastemeasurement_fill_creation_user_and_source --field creation_user
    - python manage.py wastemeasurement_fill_creation_user_and_source --field creation_source --apply
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--field",
            type=str,
            required=True,
            choices=["creation_user", "creation_source"],
            help="Field to fill: creation_user or creation_source",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="To apply changes, otherwise just show what would be done (dry run).",
            default=False,
        )

    def handle(self, *args, **options):
        field = options["field"]
        apply = options["apply"]
        logger.info(f"Start task: wastemeasurement_fill_creation_user_and_source ({field}) (apply={apply})")

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        if field == "creation_user":
            fill_creation_user(WasteMeasurement.objects, WasteMeasurement.history, apply=apply)
        elif field == "creation_source":
            fill_creation_source(apply=apply)


def fill_creation_source(apply):
    """
    Rules:
    - look at the first version of the waste measurement in the history (see get_creation_source_from_first_version)
    - else creation_source stays empty
    """
    wm_ids = list(
        WasteMeasurement.objects.filter(has_charfield_missing_query("creation_source")).values_list("id", flat=True)
    )
    logger.info(f"Found {len(wm_ids)} waste measurements with missing creation_source")
    logger.info(Counter(WasteMeasurement.objects.values_list("creation_source", flat=True)))

    first_versions = get_first_versions(WasteMeasurement.history, wm_ids)
    creation_source_by_wm_id = {}
    for wm_id in wm_ids:
        creation_source = get_creation_source_from_first_version(first_versions.get(wm_id))
        if creation_source:
            creation_source_by_wm_id[wm_id] = creation_source

    update_objects(WasteMeasurement.objects, "creation_source", creation_source_by_wm_id, apply=apply)

    wm_qs_after = WasteMeasurement.objects.exclude(has_charfield_missing_query("creation_source"))
    logger.info(f"Done! {wm_qs_after.count()} waste measurements with filled creation_source")
    logger.info(Counter(WasteMeasurement.objects.values_list("creation_source", flat=True)))
