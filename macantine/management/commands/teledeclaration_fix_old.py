from django.core.management.base import BaseCommand
from simple_history.utils import update_change_reason

from data.models import Diagnostic


class Command(BaseCommand):
    """
    Examples:
    - python manage.py teledeclaration_fix_old --command=set_canteen_id_before_v4
    - python manage.py teledeclaration_fix_old --command=set_canteen_id_before_v4 --apply
    """

    help = "One-time commands to fix old teledeclarations"

    def add_arguments(self, parser):
        parser.add_argument(
            "--command",
            type=str,
            required=True,
            choices=["set_canteen_id_before_v4"],
            help="Command to run. Options are: 'list_diagnostics_without_td', 'create",
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

    def set_canteen_id_before_v4(self, apply):
        diagnostic_updated = 0
        # teledeclaration_qs = Teledeclaration.objects.exclude(declared_data__version__gte=4)  # stored as string, harder...
        diagnostic_qs = (
            Diagnostic.objects.select_related("canteen").teledeclared().exclude(teledeclaration_version__gte=4)
        )  # 304
        print("Diagnostics teledeclared with version < 4:", diagnostic_qs.count())
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
                        diagnostic_updated += 1
                    else:
                        print(
                            f"Diagnostic {diagnostic.id} already has a canteen_id {canteen_snapshot_temp['id']}, skipping"
                        )
                else:
                    print(f"Diagnostic {diagnostic.id} has no canteen_snapshot, skipping")
            else:
                print(f"Diagnostic {diagnostic.id} has no canteen, skipping")
        print("Diagnostics updated:", diagnostic_updated)
