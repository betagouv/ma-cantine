import logging

from data.models import Diagnostic
from common.utils.commands import MaCantineBaseCommand

logger = logging.getLogger(__name__)


FIELD_LIST = (
    Diagnostic.APPRO_AGGREGATED_FIELDS
    + Diagnostic.APPRO_STATS_FIELDS
    + Diagnostic.OTHER_COMPUTED_FIELDS
    + ["satellites_nombre_repas_an_sum", "is_clean"]
)


class Command(MaCantineBaseCommand):
    """
    Goal: command to fill Diagnostic "computed" fields (see FIELD_LIST)

    Usage:
    - python manage.py diagnostic_fill_computed_fields --year 2025
    - python manage.py diagnostic_fill_computed_fields --year 2025 --apply
    - python manage.py diagnostic_fill_computed_fields --year 2025 --field pourcentage_bio --field pourcentage_egalim --apply
    """

    help = "Fill diagnostic computed fields for a given year"

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            type=int,
            required=True,
            help="Year of the teledeclaration campaign to process",
        )
        parser.add_argument(
            "--field",
            action="append",
            choices=FIELD_LIST,
            dest="field_list",
            help="Only fill this computed field (can be repeated). Default: all the computed fields",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="To apply changes, otherwise just show what would be done (dry run).",
            default=False,
        )

    def handle(self, *args, **options):
        year = options["year"]
        field_list = options["field_list"] or FIELD_LIST
        apply = options["apply"]
        logger.info(f"Start task: diagnostic_fill_computed_fields for year {year} (fields: {field_list})")

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        # all_objects: also include the diagnostics generated from a groupe diagnostic
        qs = Diagnostic.all_objects.in_year(year)

        logger.info("Step 1: find the diagnostics for the specified year")
        logger.info(f"Found {qs.count()} diagnostics for year {year}")

        logger.info("Step 2: compute (& update) the fields (both draft & teledeclared diagnostics)")
        changed_count_per_field = {field_name: 0 for field_name in field_list}
        changed_count = 0
        for index, diagnostic in enumerate(qs.iterator(), start=1):
            values_before = {field_name: getattr(diagnostic, field_name) for field_name in field_list}
            # explicit call: save() doesn't populate the computed fields of teledeclared diagnostics (frozen)
            diagnostic.populate_computed_fields()
            values_after = {field_name: getattr(diagnostic, field_name) for field_name in field_list}
            changed_field_list = [
                field_name for field_name in field_list if values_after[field_name] != values_before[field_name]
            ]
            for field_name in changed_field_list:
                changed_count_per_field[field_name] += 1
            if changed_field_list:
                changed_count += 1
                if apply:
                    # update() instead of save(): only the computed fields (populate_computed_fields() can also
                    # prefill other fields in memory), no signals, no historical record & modification_date unchanged
                    Diagnostic.all_objects.filter(id=diagnostic.id).update(
                        **{field_name: values_after[field_name] for field_name in changed_field_list}
                    )
            if index % 5000 == 0:
                logger.info(f"Processed {index} diagnostics")

        for field_name in field_list:
            if changed_count_per_field[field_name]:
                logger.info(f"Computed: {changed_count_per_field[field_name]} diagnostics with {field_name} changed")
        logger.info(f"Computed: {changed_count} diagnostics with at least one changed field")

        # Done!
        logger.info(f"Task completed: {changed_count} diagnostics {'updated' if apply else 'to update'}")
