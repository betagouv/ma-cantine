import logging

from django.core.management.base import BaseCommand

from data.models import Canteen

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Usage:
    - python manage.py canteen_fill_is_filled_field
    - python manage.py canteen_fill_is_filled_field --apply
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--apply",
            action="store_true",
            help="To apply changes, otherwise just show what would be done (dry run).",
            default=False,
        )

    def handle(self, *args, **options):
        logger.info("Start task: canteen_fill_is_filled_field")
        apply = options["apply"]

        if not apply:
            print("Dry run mode, no changes will be applied.")

        canteens_all_qs = Canteen.all_objects.all()
        logger.info(f"Found {canteens_all_qs.count()} canteens to process")

        # stats before
        canteen_is_filled_qs = canteens_all_qs.filter(is_filled=True)
        logger.info(f"Before: {canteen_is_filled_qs.count()} canteens with is_filled=True")

        if apply:
            # Step 1: reset all is_filled to False
            canteens_all_qs.update(is_filled=False)
            # Step 2: compute & update is_filled field
            canteen_is_filled_id_list = []
            for canteen in canteens_all_qs:
                if canteen._is_filled():
                    canteen_is_filled_id_list.append(canteen.id)
            # Step 3: update the field
            Canteen.all_objects.filter(id__in=canteen_is_filled_id_list).update(is_filled=True)

        # stats after
        canteen_is_filled_qs = canteens_all_qs.filter(is_filled=True)
        logger.info(f"After: {canteen_is_filled_qs.count()} canteens with is_filled=True")
