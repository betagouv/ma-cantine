import logging
from collections import Counter

from common.utils.commands import MaCantineBaseCommand
from common.utils.fill_creation import (
    fill_creation_source_api_oauth2_application,
    fill_creation_user,
    get_creation_source_from_first_version,
    get_first_versions,
    update_objects,
)
from data.models import Canteen
from data.models.creation_source import CreationSource
from data.utils import has_charfield_missing_query

logger = logging.getLogger(__name__)

FIELD_CHOICES = ["creation_user", "creation_source", "creation_source_api_oauth2_application"]


class Command(MaCantineBaseCommand):
    """
    Usage:
    - python manage.py canteen_fill_creation_user_and_source --field creation_user
    - python manage.py canteen_fill_creation_user_and_source --field creation_source --apply
    - python manage.py canteen_fill_creation_user_and_source --field creation_source_api_oauth2_application --apply

    Note: run creation_user & creation_source first (creation_source_api_oauth2_application depends on them)
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "--field",
            type=str,
            required=True,
            choices=FIELD_CHOICES,
            help=f"Field to fill: {', '.join(FIELD_CHOICES)}",
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
            fill_creation_user(Canteen.all_objects, Canteen.history, apply=apply)
        elif field == "creation_source":
            fill_creation_source(apply=apply)
        elif field == "creation_source_api_oauth2_application":
            fill_creation_source_api_oauth2_application(Canteen.all_objects, Canteen.history, apply=apply)


def fill_creation_source(apply):
    """
    Rules:
    - if import_source starts with "Cuisine centrale : ", then creation_source = "APP"
    - else if import_source is not empty, then creation_source = "IMPORT"
    - else look at the first version of the canteen in the history (see get_creation_source_from_first_version)
    - else creation_source stays empty

    Note: moved from data/migrations/0183_canteen_creation_source_populate.py
    """
    canteens = list(
        Canteen.all_objects.filter(has_charfield_missing_query("creation_source")).values_list("id", "import_source")
    )
    logger.info(f"Found {len(canteens)} canteens with missing creation_source")
    logger.info(Counter(Canteen.all_objects.values_list("creation_source", flat=True)))

    creation_source_by_canteen_id = {}
    canteen_ids_without_import_source = []
    # first set of rules: import_source
    for canteen_id, import_source in canteens:
        if import_source and import_source.startswith("Cuisine centrale : "):
            creation_source_by_canteen_id[canteen_id] = CreationSource.APP
        elif import_source:
            creation_source_by_canteen_id[canteen_id] = CreationSource.IMPORT
        else:
            canteen_ids_without_import_source.append(canteen_id)
    # second set of rules: HistoricalCanteen
    first_versions = get_first_versions(Canteen.history, canteen_ids_without_import_source)
    for canteen_id in canteen_ids_without_import_source:
        creation_source = get_creation_source_from_first_version(first_versions.get(canteen_id))
        if creation_source:
            creation_source_by_canteen_id[canteen_id] = creation_source

    update_objects(Canteen.all_objects, "creation_source", creation_source_by_canteen_id, apply=apply)

    canteen_qs_after = Canteen.all_objects.exclude(has_charfield_missing_query("creation_source"))
    logger.info(f"Done! {canteen_qs_after.count()} canteens with filled creation_source")
    logger.info(Counter(Canteen.all_objects.values_list("creation_source", flat=True)))
