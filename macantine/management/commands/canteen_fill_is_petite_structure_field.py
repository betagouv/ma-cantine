import logging

from data.models import Canteen
from common.utils.commands import MaCantineBaseCommand

logger = logging.getLogger(__name__)


class Command(MaCantineBaseCommand):
    """
    Usage:
    - python manage.py canteen_fill_is_petite_structure_field
    - python manage.py canteen_fill_is_petite_structure_field --apply
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="To apply changes, otherwise just show what would be done (dry run).",
            default=False,
        )

    def handle(self, *args, **options):
        logger.info("Start task: canteen_fill_is_petite_structure_field")
        apply = options["apply"]

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        canteens_all_qs = Canteen.all_objects.all()
        logger.info(f"Found {canteens_all_qs.count()} canteens to process")

        # stats before
        logger.info(
            f"Before: {canteens_all_qs.filter(is_petite_structure=True).count()} canteens with is_petite_structure=True"
        )

        # compute is_petite_structure
        canteen_is_petite_structure_id_list = [
            canteen.id for canteen in canteens_all_qs.iterator() if canteen._is_petite_structure()
        ]
        logger.info(f"Computed: {len(canteen_is_petite_structure_id_list)} canteens with is_petite_structure=True")

        if apply:
            # Step 1: reset all is_petite_structure to False
            canteens_all_qs.update(is_petite_structure=False)
            # Step 2: update the field
            Canteen.all_objects.filter(id__in=canteen_is_petite_structure_id_list).update(is_petite_structure=True)

        # stats after
        logger.info(
            f"After: {canteens_all_qs.filter(is_petite_structure=True).count()} canteens with is_petite_structure=True"
        )
