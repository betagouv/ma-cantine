import logging

from data.models import Canteen
from common.utils.commands import MaCantineBaseCommand

logger = logging.getLogger(__name__)


FIELD_LIST = ["is_filled", "is_clean", "is_petite_structure"]


class Command(MaCantineBaseCommand):
    """
    Goal: command to fill Canteen "computed" fields (see FIELD_LIST)

    Usage:
    - python manage.py canteen_fill_computed_fields
    - python manage.py canteen_fill_computed_fields --apply
    - python manage.py canteen_fill_computed_fields --field is_clean --apply
    """

    help = "Fill canteen computed fields"

    def add_arguments(self, parser):
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
        field_list = options["field_list"] or FIELD_LIST
        apply = options["apply"]
        logger.info(f"Start task: canteen_fill_computed_fields (fields: {field_list})")

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        # all_objects: also include the soft-deleted canteens
        qs = Canteen.all_objects.all()

        logger.info("Step 1: find the canteens")
        logger.info(f"Found {qs.count()} canteens")
        for field_name in field_list:
            logger.info(f"Before: {qs.filter(**{field_name: True}).count()} canteens with {field_name}=True")

        logger.info("Step 2: compute (& update) the fields")
        computed_true_count = {field_name: 0 for field_name in field_list}
        changed_count = 0
        for index, canteen in enumerate(qs.iterator(), start=1):
            values_before = {field_name: getattr(canteen, field_name) for field_name in field_list}
            # same as in save(), before computing the fields
            canteen.normalize_fields()
            for field_name in field_list:
                getattr(canteen, f"set_{field_name}")()
            values_after = {field_name: getattr(canteen, field_name) for field_name in field_list}
            for field_name in field_list:
                computed_true_count[field_name] += int(values_after[field_name])
            if values_after != values_before:
                changed_count += 1
                if apply:
                    # update() instead of save(): no side effects (logo optimization, geo fields, signals...),
                    # no historical record & modification_date unchanged (computed fields only)
                    Canteen.all_objects.filter(id=canteen.id).update(**values_after)
            if index % 5000 == 0:
                logger.info(f"Processed {index} canteens")

        for field_name in field_list:
            logger.info(f"Computed: {computed_true_count[field_name]} canteens with {field_name}=True")
        logger.info(f"Computed: {changed_count} canteens with at least one changed field")

        # Done!
        for field_name in field_list:
            logger.info(f"After: {qs.filter(**{field_name: True}).count()} canteens with {field_name}=True")
        logger.info(f"Task completed: {changed_count} canteens {'updated' if apply else 'to update'}")
