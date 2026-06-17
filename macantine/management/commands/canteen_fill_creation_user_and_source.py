import logging
from collections import Counter

from django.core.management.base import BaseCommand
from django.db.models import Q, Case, When, F, Value
from django.db.models.functions import Length

from data.utils import has_charfield_missing_query
from data.models import Canteen

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Usage:
    - python manage.py canteen_fill_creation_user_and_source --field creation_user
    - python manage.py canteen_fill_creation_user_and_source --field creation_source --apply
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
        logger.info(f"Start task: canteen_fill_creation_user_and_source ({field}) (apply={apply})")

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        if field == "creation_user":
            fill_creation_user(apply=apply)
        elif field == "creation_source":
            fill_creation_source(apply=apply)


def fill_creation_user(apply):
    """
    Rules:
    - if creation_user is null, empty or None, then look at the first version of the canteen in the history:
        - set creation_user to history_user
    - else creation_user stays empty
    """
    canteen_qs = Canteen.all_objects.filter(creation_user__isnull=True)
    logger.info(f"Found {canteen_qs.count()} canteens with missing creation_user")

    if apply:
        for index, canteen in enumerate(canteen_qs.all(), start=1):
            canteen_first_version = Canteen.history.filter(id=canteen.id).last()
            if not canteen.creation_user and canteen_first_version and canteen_first_version.history_type == "+":
                if canteen_first_version.history_user_id:
                    canteen.creation_user = canteen_first_version.history_user
                    Canteen.all_objects.filter(id=canteen.id).update(creation_user=canteen.creation_user)
            if index % 5000 == 0:
                logger.info(f"Processed {index} canteens")

    canteen_qs_after = Canteen.all_objects.exclude(creation_user__isnull=True)
    logger.info(f"Done! {canteen_qs_after.count()} canteens with filled creation_user")


def fill_creation_source(apply):
    """
    Rules:
    - if import_source starts with "Cuisine centrale : ", then creation_source = "APP"
    - else if import_source is not empty, then creation_source = "IMPORT"
    - else look at the first version of the canteen in the history:
        - if history_change_reason is null and history_user is staff, then creation_source = "ADMIN"
        - if history_change_reason starts with "Mass CSV import", then creation_source = "IMPORT"
        - if history_change_reason is "SessionAuthentication", then creation_source = "APP"
        - if history_change_reason is "OAuth2Authentication", then creation_source = "API"
    - else creation_source stays empty

    Note: moved from data/migrations/0183_canteen_creation_source_populate.py
    """
    canteen_qs = Canteen.all_objects.filter(has_charfield_missing_query("creation_source"))
    logger.info(f"Found {canteen_qs.count()} canteens with missing creation_source")
    logger.info(Counter(Canteen.all_objects.values_list("creation_source", flat=True)))

    if apply:
        # first set of rules: based on import_source
        canteen_qs.annotate(import_source_length=Length("import_source")).annotate(
            creation_source_annotated=Case(
                When(Q(import_source__startswith="Cuisine centrale : "), then=Value("APP")),
                When(Q(import_source_length__gt=0), then=Value("IMPORT")),
                default=Value(None),
            )
        ).update(creation_source=F("creation_source_annotated"))
        # second set of rules: HistoricalCanteen
        for index, canteen in enumerate(canteen_qs.all(), start=1):
            canteen_first_version = Canteen.history.filter(id=canteen.id).last()
            if not canteen.creation_source and canteen_first_version and canteen_first_version.history_type == "+":
                if canteen_first_version.history_change_reason is None:
                    if canteen_first_version.history_user_id and canteen_first_version.history_user.is_staff:
                        canteen.creation_source = "ADMIN"
                        Canteen.all_objects.filter(id=canteen.id).update(creation_source=canteen.creation_source)
                elif canteen_first_version.history_change_reason.startswith("Mass CSV import"):
                    canteen.creation_source = "IMPORT"
                    Canteen.all_objects.filter(id=canteen.id).update(creation_source=canteen.creation_source)
                elif canteen_first_version.history_change_reason == "SessionAuthentication":
                    canteen.creation_source = "APP"
                    Canteen.all_objects.filter(id=canteen.id).update(creation_source=canteen.creation_source)
                elif canteen_first_version.history_change_reason == "OAuth2Authentication":
                    canteen.creation_source = "API"
                    Canteen.all_objects.filter(id=canteen.id).update(creation_source=canteen.creation_source)
            if index % 5000 == 0:
                logger.info(f"Processed {index} canteens")

    canteen_qs_after = Canteen.all_objects.exclude(has_charfield_missing_query("creation_source"))
    logger.info(f"Done! {canteen_qs_after.count()} canteens with filled creation_source")
    logger.info(Counter(Canteen.all_objects.values_list("creation_source", flat=True)))
