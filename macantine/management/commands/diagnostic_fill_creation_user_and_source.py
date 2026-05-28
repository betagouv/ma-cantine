import logging
from collections import Counter

from django.core.management.base import BaseCommand
from django.db.models import Q, Case, When, F, Value
from django.db.models.functions import Length

from data.utils import has_charfield_missing_query
from data.models import Diagnostic

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Usage:
    - python manage.py diagnostic_fill_creation_user_and_source --field creation_user
    - python manage.py diagnostic_fill_creation_user_and_source --field creation_source --apply
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
        logger.info(f"Start task: diagnostic_fill_creation_user_and_source ({field}) (apply={apply})")

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        if field == "creation_user":
            fill_creation_user(apply=apply)
        elif field == "creation_source":
            fill_creation_source(apply=apply)


def fill_creation_user(apply):
    """
    Rules:
    - if creation_user is null, empty or None, then look at the first version of the diagnostic in the history:
        - set creation_user to history_user
    - else creation_user stays empty
    """
    diagnostic_qs = Diagnostic.objects.filter(creation_user__isnull=True)  # exclude 1td1site
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with missing creation_user")

    if apply:
        for index, diagnostic in enumerate(diagnostic_qs.all(), start=1):
            diagnostic_first_version = Diagnostic.history.filter(id=diagnostic.id).last()
            if (
                not diagnostic.creation_user
                and diagnostic_first_version
                and diagnostic_first_version.history_type == "+"
            ):
                if diagnostic_first_version.history_user_id:
                    diagnostic.creation_user = diagnostic_first_version.history_user
                    Diagnostic.objects.filter(id=diagnostic.id).update(creation_user=diagnostic.creation_user)
            if index % 5000 == 0:
                logger.info(f"Processed {index} diagnostics")

    diagnostic_qs_after = Diagnostic.objects.exclude(creation_user__isnull=True)
    logger.info(f"Done! {diagnostic_qs_after.count()} diagnostics with filled creation_user")


def fill_creation_source(apply):
    """
    Rules:
    - if creation_mtm_source is not empty, then creation_source = "APP"
    - else, look at the first version of the diagnostic in the history:
        - if history_change_reason is null and history_user is staff, then creation_source = "ADMIN"
        - else if history_change_reason starts with "Mass CSV import", then creation_source = "IMPORT"
        - else if history_change_reason is "SessionAuthentication", then creation_source = "APP"
        - else if history_change_reason is "OAuth2Authentication", then creation_source = "API"
    - else creation_source stays empty

    Note: moved from data/migrations/0184_diagnostic_creation_source_populate.py
    """
    diagnostic_qs = Diagnostic.objects.filter(has_charfield_missing_query("creation_source"))
    logger.info(f"Found {diagnostic_qs.count()} diagnostics with missing creation_source")
    logger.info(Counter(Diagnostic.objects.values_list("creation_source", flat=True)))

    if apply:
        # first set of rules:
        diagnostic_qs.annotate(creation_mtm_source_length=Length("creation_mtm_source")).annotate(
            creation_source_annotated=Case(
                When(Q(creation_mtm_source_length__gt=0), then=Value("APP")),
                default=Value(None),
            )
        ).update(creation_source=F("creation_source_annotated"))
        # second set of rules: HistoricalDiagnostic
        for index, diagnostic in enumerate(diagnostic_qs.all(), start=1):
            diagnostic_first_version = Diagnostic.history.filter(id=diagnostic.id).last()
            if (
                not diagnostic.creation_source
                and diagnostic_first_version
                and diagnostic_first_version.history_type == "+"
            ):
                if diagnostic_first_version.history_change_reason is None:
                    if diagnostic_first_version.history_user_id and diagnostic_first_version.history_user.is_staff:
                        Diagnostic.objects.filter(id=diagnostic.id).update(creation_source="ADMIN")
                elif diagnostic_first_version.history_change_reason.startswith("Mass CSV import"):
                    Diagnostic.objects.filter(id=diagnostic.id).update(creation_source="IMPORT")
                elif diagnostic_first_version.history_change_reason == "SessionAuthentication":
                    Diagnostic.objects.filter(id=diagnostic.id).update(creation_source="APP")
                elif diagnostic_first_version.history_change_reason == "OAuth2Authentication":
                    Diagnostic.objects.filter(id=diagnostic.id).update(creation_source="API")
                if index % 5000 == 0:
                    logger.info(f"Processed {index} diagnostics")

    diagnostic_qs_after = Diagnostic.objects.exclude(has_charfield_missing_query("creation_source"))
    logger.info(f"Done! {diagnostic_qs_after.count()} diagnostics with filled creation_source")
    logger.info(Counter(Diagnostic.objects.values_list("creation_source", flat=True)))
