"""
Why this script?
Some canteens were previous imported but need to be removed.

How to run?
python manage.py canteen_delete --canteen-siret-list 92341284500011,23456789012345

Ran on 2025-04-24
"""

from django.core.management.base import BaseCommand

from data.models import Canteen, Diagnostic, Teledeclaration


class Command(BaseCommand):
    help = "Soft delete a specified list of canteens"

    def add_arguments(self, parser):
        parser.add_argument(
            "--canteen-siret-list",
            dest="canteen_siret_list",
            type=str,
            required=True,
            help="Comma-seperated list of canteen SIRETs to process",
        )

    def handle(self, *args, **options):
        # init
        print("Starting canteen soft delete task")
        canteen_deleted_count = 0
        canteen_siret_list = options["canteen_siret_list"].split(",")
        print("SIRET in input list:", len(canteen_siret_list))

        canteen_qs = Canteen.objects.filter(siret__in=canteen_siret_list)
        print("Canteens found:", canteen_qs.count())

        # loop on each canteen
        for canteen in canteen_qs:
            # canteen must not have any diagnostics or teledeclarations
            canteen_diagnostic_count = Diagnostic.objects.filter(canteen=canteen).count()
            if canteen_diagnostic_count > 0:
                print(f"Cannot delete canteen {canteen.siret} because it has {canteen_diagnostic_count} diagnostics")
                continue  # skip canteen
            canteen_td_count = Teledeclaration.objects.filter(canteen=canteen).count()
            if canteen_td_count > 0:
                print(f"Cannot delete canteen {canteen.siret} because it has {canteen_td_count} teledeclarations")
                continue  # skip canteen
            # soft delete
            canteen.delete()
            canteen_deleted_count += 1

        print("Done!")
        print("Canteens deleted:", canteen_deleted_count)
