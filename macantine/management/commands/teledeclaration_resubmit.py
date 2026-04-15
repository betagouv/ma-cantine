"""
Why this script?
We updated/fixed the data of some canteens after they teledeclared.
To reflect the changes in the Diagnostic objects, we need to cancel and re-submit these teledeclarations.

How to run?
python manage.py teledeclaration_resubmit --year 2024 --teledeclaration-id-list 123,456,789

Ran on 2025-04-18 (2024 campaign)
Ran on 2026-04-15 (last day of 2025 campaign)
"""

import logging

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError

from data.models import Diagnostic


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Resubmit teledeclarations for a specified list of diagnostics"

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            dest="year",
            type=int,
            required=True,
            help="Year of the teledeclaration campaign to process",
        )
        parser.add_argument(
            "--teledeclaration-id-list",
            dest="teledeclaration_id_list",
            type=str,
            required=True,
            help="Comma-seperated list of diagnostic IDs to process",
        )

    def handle(self, *args, **options):
        # init
        logger.info("Starting task: teledeclaration resubmit")
        teledeclaration_resubmitted_count = 0
        year = options["year"]
        logger.info(f"Year in input: {year}")
        teledeclaration_id_list = options["teledeclaration_id_list"].split(",")
        logger.info(f"Diagnostic IDs in input list: {len(teledeclaration_id_list)}")

        # queryset
        diagnostics_qs = Diagnostic.objects.filter(id__in=teledeclaration_id_list)
        logger.info(f"Diagnostics (teledeclared) found: {diagnostics_qs.count()}")

        # loop on each diagnostic
        for diagnostic in diagnostics_qs:
            diagnostic_applicant = diagnostic.applicant
            # diagnostic must be in the right year
            if diagnostic.year != year:
                logger.warning(f"Diagnostic {diagnostic.id} is from year {diagnostic.year}, expected {year}, skipping")
                continue
            # diagnostic must be submitted
            if not diagnostic.is_teledeclared:
                logger.warning(f"Diagnostic {diagnostic.id} is not teledeclared, skipping")
                continue
            # cancel TD
            diagnostic.cancel()
            # recreate TD
            try:
                diagnostic.teledeclare(applicant=diagnostic_applicant)
                teledeclaration_resubmitted_count += 1
            except ValidationError as e:
                logger.error(f"Error teledeclaring diagnostic {diagnostic.id}: {e}")
                continue  # skip to next diagnostic

        result = (
            f"Teledeclarations resubmitted: {teledeclaration_resubmitted_count} out of {len(teledeclaration_id_list)}"
        )
        logger.info(f"Task completed: {result}")
        return result
