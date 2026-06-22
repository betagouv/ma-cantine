import logging
from collections import Counter

from django.core.management.base import BaseCommand

from data.utils import has_charfield_missing_query
from data.models import WasteMeasurement

logger = logging.getLogger(__name__)


class Command(BaseCommand):
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
            fill_creation_user(apply=apply)
        elif field == "creation_source":
            fill_creation_source(apply=apply)


def fill_creation_user(apply):
    """
    Rules:
    - if creation_user is null, empty or None, then look at the first version of the wastemeasurement in the history:
        - set creation_user to history_user
    - else creation_user stays empty
    """
    wm_qs = WasteMeasurement.objects.filter(creation_user__isnull=True)
    logger.info(f"Found {wm_qs.count()} waste measurements with missing creation_user")

    if apply:
        for index, wm in enumerate(wm_qs.all(), start=1):
            wm_first_version = WasteMeasurement.history.filter(id=wm.id).last()
            if not wm.creation_user and wm_first_version and wm_first_version.history_type == "+":
                if wm_first_version.history_user_id:
                    wm.creation_user = wm_first_version.history_user
                    WasteMeasurement.objects.filter(id=wm.id).update(creation_user=wm.creation_user)
            if index % 5000 == 0:
                logger.info(f"Processed {index} waste measurements")

    wm_qs_after = WasteMeasurement.objects.exclude(creation_user__isnull=True)
    logger.info(f"Done! {wm_qs_after.count()} waste measurements with filled creation_user")


def fill_creation_source(apply):
    """
    Rules:
    - if creation_source is null, empty or None, then look at the first version of the wastemeasurement in the history:
        - if history_change_reason is null and history_user is staff, then creation_source = "ADMIN"
        - else if history_change_reason starts with "Mass CSV import", then creation_source = "IMPORT"
        - else if history_change_reason is "SessionAuthentication", then creation_source = "APP"
        - else if history_change_reason is "OAuth2Authentication", then creation_source = "API"
    - else creation_source stays empty
    """
    wm_qs = WasteMeasurement.objects.filter(has_charfield_missing_query("creation_source"))
    logger.info(f"Found {wm_qs.count()} waste measurements with missing creation_source")
    logger.info(Counter(WasteMeasurement.objects.values_list("creation_source", flat=True)))

    if apply:
        for index, wm in enumerate(wm_qs.all(), start=1):
            wm_first_version = WasteMeasurement.history.filter(id=wm.id).last()
            if not wm.creation_source and wm_first_version and wm_first_version.history_type == "+":
                if wm_first_version.history_change_reason is None:
                    if wm_first_version.history_user_id and wm_first_version.history_user.is_staff:
                        WasteMeasurement.objects.filter(id=wm.id).update(creation_source="ADMIN")
                elif wm_first_version.history_change_reason == "SessionAuthentication":
                    WasteMeasurement.objects.filter(id=wm.id).update(creation_source="APP")
                elif wm_first_version.history_change_reason == "OAuth2Authentication":
                    WasteMeasurement.objects.filter(id=wm.id).update(creation_source="API")
                if index % 5000 == 0:
                    logger.info(f"Processed {index} waste measurements")

    wm_qs_after = WasteMeasurement.objects.exclude(has_charfield_missing_query("creation_source"))
    logger.info(f"Done! {wm_qs_after.count()} waste measurements with filled creation_source")
    logger.info(Counter(WasteMeasurement.objects.values_list("creation_source", flat=True)))
