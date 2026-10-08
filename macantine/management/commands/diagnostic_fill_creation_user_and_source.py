import logging
from collections import Counter

from common.utils.commands import MaCantineBaseCommand
from common.utils.fill_creation import (
    fill_creation_user,
    get_creation_source_from_first_version,
    get_first_versions,
    update_objects,
)
from data.models import Diagnostic
from data.models.creation_source import CreationSource
from data.utils import has_charfield_missing_query

logger = logging.getLogger(__name__)


class Command(MaCantineBaseCommand):
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
            fill_creation_user(Diagnostic.objects, Diagnostic.history, apply=apply)  # excludes 1td1site
        elif field == "creation_source":
            fill_creation_source(apply=apply)


def fill_creation_source(apply):
    """
    Rules:
    - if creation_mtm_source is not empty, then creation_source = "APP"
    - else look at the first version of the diagnostic in the history (see get_creation_source_from_first_version)
    - else creation_source stays empty

    Note: moved from data/migrations/0184_diagnostic_creation_source_populate.py
    """
    diagnostics = list(
        Diagnostic.objects.filter(has_charfield_missing_query("creation_source")).values_list(
            "id", "creation_mtm_source"
        )
    )
    logger.info(f"Found {len(diagnostics)} diagnostics with missing creation_source")
    logger.info(Counter(Diagnostic.objects.values_list("creation_source", flat=True)))

    creation_source_by_diagnostic_id = {}
    diagnostic_ids_without_mtm_source = []
    # first set of rules: creation_mtm_source
    for diagnostic_id, creation_mtm_source in diagnostics:
        if creation_mtm_source:
            creation_source_by_diagnostic_id[diagnostic_id] = CreationSource.APP
        else:
            diagnostic_ids_without_mtm_source.append(diagnostic_id)
    # second set of rules: HistoricalDiagnostic
    first_versions = get_first_versions(Diagnostic.history, diagnostic_ids_without_mtm_source)
    for diagnostic_id in diagnostic_ids_without_mtm_source:
        creation_source = get_creation_source_from_first_version(first_versions.get(diagnostic_id))
        if creation_source:
            creation_source_by_diagnostic_id[diagnostic_id] = creation_source

    update_objects(Diagnostic.objects, "creation_source", creation_source_by_diagnostic_id, apply=apply)

    diagnostic_qs_after = Diagnostic.objects.exclude(has_charfield_missing_query("creation_source"))
    logger.info(f"Done! {diagnostic_qs_after.count()} diagnostics with filled creation_source")
    logger.info(Counter(Diagnostic.objects.values_list("creation_source", flat=True)))
