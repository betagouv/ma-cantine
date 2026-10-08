import logging

from common.utils.commands import MaCantineBaseCommand
from common.utils.fill_creation import fill_creation_source_api_oauth2_application
from data.models import Purchase

logger = logging.getLogger(__name__)

FIELD_CHOICES = ["creation_source_api_oauth2_application"]


class Command(MaCantineBaseCommand):
    """
    Usage:
    - python manage.py purchase_fill_creation_user_and_source --field creation_source_api_oauth2_application
    - python manage.py purchase_fill_creation_user_and_source --field creation_source_api_oauth2_application --apply

    Note: Purchase has no history, so creation_user & creation_source cannot be filled from it
    (and creation_source_api_oauth2_application can only be filled from the OAuth2 tokens of the creation_user)
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
        logger.info(f"Start task: purchase_fill_creation_user_and_source ({field}) (apply={apply})")

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        if field == "creation_source_api_oauth2_application":
            fill_creation_source_api_oauth2_application(Purchase.all_objects, None, apply=apply)
