"""
Why this script?
We updated/fixed the data of some canteens after they teledeclared.
To reflect the changes in the Teledeclaration objects, we need to cancel and re-submit these teledeclarations.

Ran on 2025-04-16 (Campaign for 2024)
"""

from django.core.management.base import BaseCommand

from data.models import Canteen, Teledeclaration

CANTEEN_SIRET_LIST = ["21380397600017"]
YEAR = 2024


class Command(BaseCommand):
    help = "Resubmit teledeclarations for a specified list of canteens"

    def handle(self, *args, **options):
        # init
        teledeclaration_resubmitted_count = 0
        canteen_qs = Canteen.objects.filter(siret__in=CANTEEN_SIRET_LIST)

        # loop on each canteen
        for canteen in canteen_qs:
            # canteen must have submitted a TD during the campaign
            canteen_td_submitted_for_year_qs = Teledeclaration.objects.filter(canteen=canteen).submitted_for_year(YEAR)
            if not canteen_td_submitted_for_year_qs.exists():
                print(f"No teledeclaration for canteen {canteen.siret} for year {YEAR}")
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
                print(f"Failed to resubmit teledeclaration for canteen {canteen.siret} for year {YEAR}")
                print(e)
                continue

        print("Done!")
        print("SIRET in input list:", len(CANTEEN_SIRET_LIST))
        print("Canteen found", canteen_qs.count())
        print("Teledeclarations resubmitted:", teledeclaration_resubmitted_count)
