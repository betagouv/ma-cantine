"""
Why this script?
We updated/fixed the data of some canteens after they teledeclared.
To reflect the changes in the Teledeclaration objects, we need to cancel and re-submit these teledeclarations.

How to run?
python manage.py canteen_teledeclaration_resubmit --year 2024 --canteen-siret-list 12345678901234,23456789012345

Ran on 2025-04-18 (Campaign for 2024)
"""

from django.core.management.base import BaseCommand

from data.models import Canteen, Teledeclaration


class Command(BaseCommand):
    help = "Resubmit teledeclarations for a specified list of canteens"

    def add_arguments(self, parser):
        parser.add_argument(
            "--year",
            dest="year",
            type=int,
            required=True,
            help="Year of the teledeclaration campaign to process",
        )
        parser.add_argument(
            "--canteen-siret-list",
            dest="canteen_siret_list",
            type=str,
            required=True,
            help="Comma-seperated list of canteen SIRETs to process",
        )

    def handle(self, *args, **options):
        # init
        print("Starting teledeclaration resubmit task")
        teledeclaration_resubmitted_count = 0
        year = options["year"]
        print("Year in input:", year)
        canteen_siret_list = options["canteen_siret_list"].split(",")
        print("SIRET in input list:", len(canteen_siret_list))

        canteen_qs = Canteen.objects.filter(siret__in=canteen_siret_list)
        print("Canteens found:", canteen_qs.count())

        # loop on each canteen
        for canteen in canteen_qs:
            # canteen must have submitted a TD during the campaign
            canteen_td_submitted_for_year_qs = Teledeclaration.objects.filter(canteen=canteen).submitted_for_year(year)
            if not canteen_td_submitted_for_year_qs.exists():
                print(f"No teledeclaration for canteen {canteen.siret} for year {year}")
                continue  # skip canteen
            canteen_td_submitted_for_year = canteen_td_submitted_for_year_qs.first()
            # cancel TD
            canteen_td_submitted_for_year.cancel()
            # recreate TD
            try:
                Teledeclaration.create_from_diagnostic(
                    diagnostic=canteen_td_submitted_for_year.diagnostic,
                    applicant=canteen_td_submitted_for_year.applicant,
                )
                teledeclaration_resubmitted_count += 1
            except Exception as e:
                print(f"Failed to resubmit teledeclaration for canteen {canteen.siret} for year {year}")
                print(e)
                continue

        print("Done!")
        print("Teledeclarations resubmitted:", teledeclaration_resubmitted_count)
