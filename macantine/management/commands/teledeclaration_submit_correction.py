"""
Why this script?
During the correction campaign, some users will cancel their teledeclaration to make some changes.
But not all of them will actually re-submit their teledeclaration after making the changes.

How to run?
python manage.py teledeclaration_submit_correction --year 2025
"""

import logging

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from simple_history.utils import update_change_reason

from data.models import Diagnostic


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Submit CORRECTION teledeclarations (during the correction campaign)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            dest="year",
            type=int,
            required=True,
            help="Year of the teledeclaration campaign to process",
        )

    def handle(self, *args, **options):
        # init
        logger.info("Starting task: teledeclaration submit correction")
        teledeclaration_correction_submitted_count = 0
        year = options["year"]
        logger.info(f"Year in input: {year}")

        # queryset
        diagnostics_qs = Diagnostic.objects.filter(year=year).filter(status=Diagnostic.DiagnosticStatus.CORRECTION)
        logger.info(f"Diagnostics (correction) found: {diagnostics_qs.count()}")

        # loop on each diagnostic
        for diagnostic in diagnostics_qs:
            # get the (previous) applicant
            diagnostic_applicant = diagnostic.history.first().applicant
            # teledeclare
            try:
                diagnostic.teledeclare(applicant=diagnostic_applicant)
                update_change_reason(diagnostic, "Script: teledeclaration_submit_correction")
                teledeclaration_correction_submitted_count += 1
            except (AttributeError, ValidationError) as e:
                logger.error(f"Error teledeclaring diagnostic {diagnostic.id}: {e}")
                continue  # skip to next diagnostic

        result = f"Teledeclarations submitted (correction): {teledeclaration_correction_submitted_count} out of {diagnostics_qs.count()} diagnostics in correction status for year {year}"
        logger.info(f"Task completed: {result}")
        return result
