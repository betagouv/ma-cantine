from collections import Counter

from django.core.management.base import BaseCommand
from django.db.models import Func, IntegerField
from simple_history.utils import update_change_reason

from data.models import Canteen, Diagnostic


class Command(BaseCommand):
    """
    Usage:
    - python manage.py teledeclaration_fix_old --command set_canteen_id_before_v4
    - python manage.py teledeclaration_fix_old --command set_canteen_id_before_v4 --apply
    - python manage.py teledeclaration_fix_old --command recreate_canteen_hard_deleted
    - python manage.py teledeclaration_fix_old --command recreate_canteen_hard_deleted --apply
    """

    help = "One-time commands to fix old teledeclarations"

    def add_arguments(self, parser):
        parser.add_argument(
            "--command",
            type=str,
            required=True,
            choices=["set_canteen_id_before_v4", "recreate_canteen_hard_deleted"],
            help="Command to run. Options are: 'set_canteen_id_before_v4', 'recreate_canteen_hard_deleted'",
        )
        parser.add_argument(
            "--apply",
            action="store_true",
            help="To apply changes, otherwise just show what would be done (dry run).",
            default=False,
        )

    def handle(self, *args, **options):
        # init
        print("Starting teledeclaration fix task")
        command = options["command"]
        apply = options["apply"]

        if not apply:
            print("Dry run mode, no changes will be applied.")

        if command == "set_canteen_id_before_v4":
            self.set_canteen_id_before_v4(apply)
        elif command == "recreate_canteen_hard_deleted":
            self.recreate_canteen_hard_deleted(apply)

    def set_canteen_id_before_v4(self, apply):
        diagnostic_updated_count = 0
        # teledeclaration_qs = Teledeclaration.objects.exclude(declared_data__version__gte=4)  # stored as string, harder...
        diagnostic_qs = (
            Diagnostic.objects.select_related("canteen").teledeclared().exclude(teledeclaration_version__gte=4)
        )
        print("Diagnostics teledeclared with version < 4:", diagnostic_qs.count())
        print("List of versions found:", Counter(diagnostic_qs.values_list("teledeclaration_version", flat=True)))
        print("List of years found:", Counter(diagnostic_qs.values_list("year", flat=True)))

        for diagnostic in diagnostic_qs:
            if diagnostic.canteen:
                canteen_snapshot_temp = diagnostic.canteen_snapshot
                if canteen_snapshot_temp:
                    if "id" not in canteen_snapshot_temp:
                        if apply:
                            canteen_snapshot_temp["id"] = diagnostic.canteen.id
                            diagnostic.canteen_snapshot = canteen_snapshot_temp
                            diagnostic.save(update_fields=["canteen_snapshot"])
                            update_change_reason(diagnostic, "Script: set missing canteen_id in canteen_snapshot")
                            # TODO?? also update the Teledeclaration object
                        diagnostic_updated_count += 1
                    else:
                        print(
                            f"Diagnostic {diagnostic.id} already has a canteen_id {canteen_snapshot_temp['id']}, skipping"
                        )
                else:
                    print(f"Diagnostic {diagnostic.id} has no canteen_snapshot, skipping")
            else:
                print(f"Diagnostic {diagnostic.id} has no canteen, skipping")
        print("Done! Diagnostics updated:", diagnostic_updated_count)

    def recreate_canteen_hard_deleted(self, apply):
        diagnostic_qs = (
            Diagnostic.objects.teledeclared()
            .annotate(
                satellites_count=Func(
                    "satellites_snapshot", function="jsonb_array_length", output_field=IntegerField()
                )
            )
            .filter(satellites_count__gt=0)
            .order_by("-teledeclaration_date")  # most recent first
        )
        print("Diagnostics teledeclared with satellites_snapshot:", diagnostic_qs.count())

        canteens_created_count = 0
        for diagnostic in diagnostic_qs:
            for canteen_satellite in diagnostic.satellites_snapshot:
                canteen_id = canteen_satellite.get("id")
                canteen_siret = canteen_satellite.get("siret")
                if canteen_id:
                    canteen_exists = Canteen.all_objects.filter(id=canteen_id).exists()
                    if canteen_exists:
                        continue
                    else:
                        print(
                            f"Canteen {canteen_id} from Diagnostic {diagnostic.id} (year {diagnostic.year} / teledeclaration_id {diagnostic.teledeclaration_id}) does not exist."
                        )
                        canteen_exists_by_siret = Canteen.all_objects.filter(siret=canteen_siret).exists()
                        if canteen_exists_by_siret:
                            print(
                                f"But a canteen with the same SIRET {canteen_siret} exists, skipping to avoid duplicates."
                            )
                        else:
                            print(
                                f"Canteen {canteen_id} from Diagnostic {diagnostic.id} with SIRET {canteen_siret} still does not exist, let's recreate it!"
                            )
                            if apply:
                                new_canteen = Canteen()
                                # 2021 info
                                # nothing, we didn't snapshot satellites at that time
                                # 2022-2023-2024 info
                                new_canteen.pk = canteen_satellite.get("id")
                                new_canteen.siret = canteen_satellite.get("siret")
                                new_canteen.name = canteen_satellite.get("name")
                                new_canteen.daily_meal_count = canteen_satellite.get("daily_meal_count")
                                new_canteen.yearly_meal_count = canteen_satellite.get("yearly_meal_count")
                                # additional info
                                new_canteen.production_type = Canteen.ProductionType.ON_SITE_CENTRAL
                                new_canteen.central_producer_siret = diagnostic.canteen_snapshot.get("siret")
                                # soft-delete the canteen (set to the last day of the teledeclaration year)
                                new_canteen.deletion_date = diagnostic.teledeclaration_date.replace(month=12, day=31)
                                new_canteen.save()
                                update_change_reason(
                                    new_canteen,
                                    f"Script: recreate_canteen_hard_deleted (diagnostic_id {diagnostic.id})",
                                )
                                for sector in canteen_satellite.get("sectors", []):
                                    new_canteen.sectors.add(sector["id"])
                            canteens_created_count += 1
                else:
                    print(f"Canteen satellite in Diagnostic {diagnostic.id} has no id, skipping")

        print("Done! Canteens recreated:", canteens_created_count)
