import logging
from collections import Counter

from django.core.management.base import BaseCommand
from django.db.models import Q, Case, When, F, Value
from django.db.models.functions import Length

from data.utils import has_charfield_missing_query
from data.models import Purchase

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Usage:
    - python manage.py purchase_fill_creation_user_and_source --field creation_user
    - python manage.py purchase_fill_creation_user_and_source --field creation_source --apply
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
        logger.info(f"Start task: purchase_fill_creation_user_and_source ({field}) (apply={apply})")

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        if field == "creation_user":
            fill_creation_user(apply=apply)
        elif field == "creation_source":
            fill_creation_source(apply=apply)


def fill_creation_user(apply):
    """
    We don't have historisation for Purchase...
    """
    pass


def fill_creation_source(apply):
    """
    Rules:
    - if import_source is "Duplication", then creation_source is "APP"
    - if import_source is "Import du fichier CSV" or has the length of a uuid4 (32), then creation_source is "IMPORT"
    - else creation_source stays empty

    Note: moved from data/migrations/0185_purchase_creation_source_populate.py
    """
    purchase_qs = Purchase.all_objects.filter(has_charfield_missing_query("creation_source"))
    logger.info(f"Found {purchase_qs.count()} purchases with missing creation_source")
    logger.info(Counter(Purchase.all_objects.values_list("creation_source", flat=True)))

    if apply:
        # first set of rules: based on import_source
        purchase_qs.annotate(import_source_length=Length("import_source")).annotate(
            creation_source_annotated=Case(
                When(Q(import_source="Duplication"), then=Value("APP")),
                When(Q(import_source="Import du fichier CSV"), then=Value("IMPORT")),
                When(Q(import_source_length=32), then=Value("IMPORT")),  # file uuid4
                default=Value(None),
            )
        ).update(creation_source=F("creation_source_annotated"))

    purchase_qs_after = Purchase.all_objects.exclude(has_charfield_missing_query("creation_source"))
    logger.info(f"Done! {purchase_qs_after.count()} purchases with filled creation_source")
    logger.info(Counter(Purchase.all_objects.values_list("creation_source", flat=True)))
