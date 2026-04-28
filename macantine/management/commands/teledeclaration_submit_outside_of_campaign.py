"""
Why this script?
During or after the teledeclaration campaign, we might want to EXCEPTIONNALY submit some diagnostics.
- DRAFT diagnostics: only if the campaign has ended (otherwise users can submit them by themselves)
- CORRECTION diagnostics: only if the correction campaign has ended (otherwise users can submit them by themselves)
- diagnostics must be from the right year

How to run?
python manage.py teledeclaration_submit_outside_of_campaign --year 2025 --diagnostic-id-list 123,456,789 --applicant-id 42
python manage.py teledeclaration_submit_outside_of_campaign --year 2025 --diagnostic-id-list 123,456,789 --applicant-id 42 --apply
"""

import logging

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from simple_history.utils import update_change_reason
from django.utils import timezone

from data.models import Diagnostic, User
from macantine.utils import (
    get_year_campaign_start_date,
    get_year_campaign_end_date_or_today_date,
    get_year_correction_end_date_or_campaign_end_date_or_today_date,
)


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Submit teledeclarations outside of the campaign"

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            type=int,
            required=True,
            help="Year of the teledeclaration campaign to process",
        )
        parser.add_argument(
            "--diagnostic-id-list",
            dest="diagnostic_id_list",
            type=str,
            required=True,
            help="Comma-separated list of diagnostic IDs to process",
        )
        parser.add_argument(
            "--applicant-id",
            dest="applicant_id",
            type=int,
            required=True,
            help="ID of the applicant (User) to set when teledeclaring",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="To apply changes, otherwise just show what would be done (dry run).",
            default=False,
        )

    def handle(self, *args, **options):
        # init
        logger.info("Starting task: teledeclaration submit outside of campaign")
        teledeclaration_submitted_count = 0
        year = options["year"]
        logger.info(f"Year in input: {year}")
        diagnostic_id_list = options["diagnostic_id_list"].split(",")
        logger.info(f"Diagnostic IDs in input list: {len(diagnostic_id_list)}")
        applicant_id = options["applicant_id"]
        logger.info(f"Applicant ID in input: {applicant_id}")
        apply = options["apply"]
        now = timezone.now()

        if not apply:
            logger.info("Dry run mode, no changes will be applied.")

        # queryset
        diagnostics_qs = Diagnostic.objects.filter(id__in=diagnostic_id_list)
        logger.info(f"Diagnostics found: {diagnostics_qs.count()}")

        applicant = User.objects.get(id=applicant_id)
        logger.info(f"Applicant found: {applicant}")

        if now < get_year_campaign_start_date(year):
            logger.error(
                f"The campaign for year {year} has not started yet. Start date: {get_year_campaign_start_date(year)}. Aborting."
            )
            return

        # loop on each diagnostic
        for diagnostic in diagnostics_qs:
            # diagnostic must be in the right year
            if diagnostic.year != year:
                logger.warning(f"Diagnostic {diagnostic.id} is from year {diagnostic.year}, expected {year}, skipping")
                continue
            # diagnostic must not be submitted
            if diagnostic.is_teledeclared:
                logger.warning(f"Diagnostic {diagnostic.id} is already teledeclared, skipping")
                continue
            # diagnostic DRAFT: must be after campaign end date
            if diagnostic.status == Diagnostic.DiagnosticStatus.DRAFT:
                if now < get_year_campaign_end_date_or_today_date(year):
                    logger.warning(
                        f"Diagnostic {diagnostic.id} is in DRAFT status but the campaign for year {year} has not ended yet, skipping"
                    )
                    continue
            # diagnostic CORRECTION: must be after campaign end date
            if diagnostic.status == Diagnostic.DiagnosticStatus.CORRECTION:
                if now < get_year_correction_end_date_or_campaign_end_date_or_today_date(year):
                    logger.warning(
                        f"Diagnostic {diagnostic.id} is in CORRECTION status but the correction campaign for year {year} has not ended yet, skipping"
                    )
                    continue
            # teledeclare
            if apply:
                try:
                    diagnostic.teledeclare(applicant=applicant, skip_validations=True)
                    update_change_reason(diagnostic, "Script: teledeclaration_submit_outside_of_campaign")
                    teledeclaration_submitted_count += 1
                except (AttributeError, ValidationError) as e:
                    logger.error(f"Error teledeclaring diagnostic {diagnostic.id}: {e}")
                    continue  # skip to next diagnostic

        result = f"Teledeclarations submitted (outside of campaign): {teledeclaration_submitted_count} out of {diagnostics_qs.count()} for year {year}"
        logger.info(f"Task completed: {result}")
        return result
