from collections import Counter

from django.core.management.base import BaseCommand
from django.db.models import Func, IntegerField
from simple_history.utils import update_change_reason

from common.api.datagouv import map_pat_list_to_communes_insee_code
from common.api.decoupage_administratif import map_communes_infos
from data.models import Canteen, Diagnostic
from data.models.sector import get_sector_list_from_old_sector_dict_list


class Command(BaseCommand):
    """
    set_canteen_id_before_v4
    - Description: dans les premières versions de la télédéclaration (avant v4), le canteen_id n'était pas stocké dans le canteen_snapshot du diagnostic. On peut le récupérer via la FK vers Canteen.
    - Usage:
        - python manage.py teledeclaration_fix_old --command set_canteen_id_before_v4
        - python manage.py teledeclaration_fix_old --command set_canteen_id_before_v4 --apply

    recreate_canteen_hard_deleted
    - Description: certains diagnostics télédéclarés font référence à des cantines supprimées (dans le satellite_snapshot). On recréé celles dont le SIRET n'existe pas déjà dans la base.
    - Usage:
        - python manage.py teledeclaration_fix_old --command recreate_canteen_hard_deleted
        - python manage.py teledeclaration_fix_old --command recreate_canteen_hard_deleted --apply

    set_canteen_snapshot_sector_list_from_sectors_m2m
    - Description: durant l'année 2025 la relation M2M entre Canteen et Sector a été remplacée par un ChoiceArrayField. Pour les versions de TD antérieure et égale à v15, cette relation M2M était donc stockée dans le canteen_snapshot "sectors", mais à partir de la v16 cela a été remplacé par le nouveau ChoiceArrayField "sector_list".
    - Usage:
        - python manage.py teledeclaration_fix_old --command set_canteen_snapshot_sector_list_from_sectors_m2m
        - python manage.py teledeclaration_fix_old --command set_canteen_snapshot_sector_list_from_sectors_m2m --apply

    set_satellites_snapshot_sector_list_from_sectors_m2m
    - Description: durant l'année 2025 la relation M2M entre Canteen et Sector a été remplacée par un ChoiceArrayField. Pour les versions de TD antérieure et égale à v15, cette relation M2M était donc stockée dans le satellites_snapshot "sectors", mais à partir de la v16 cela a été remplacé par le nouveau ChoiceArrayField "sector_list".
    - Usage:
        - python manage.py teledeclaration_fix_old --command set_satellites_snapshot_sector_list_from_sectors_m2m
        - python manage.py teledeclaration_fix_old --command set_satellites_snapshot_sector_list_from_sectors_m2m --apply

    set_canteen_snapshot_epci_and_pat_list_from_city_insee_code
    - Description: jusqu'à 2025, on n'avait pas toutes les données géo dans les canteen_snapshot. On avait city_insee_code, department & region. Mais pas epci ni pat_list.
    - Usage:
        - python manage.py teledeclaration_fix_old --command set_canteen_snapshot_epci_and_pat_list_from_city_insee_code
        - python manage.py teledeclaration_fix_old --command set_canteen_snapshot_epci_and_pat_list_from_city_insee_code --apply
    """

    help = "One-time commands to fix old teledeclarations"

    def add_arguments(self, parser):
        parser.add_argument(
            "--command",
            type=str,
            required=True,
            choices=[
                "set_canteen_id_before_v4",
                "recreate_canteen_hard_deleted",
                "set_canteen_snapshot_sector_list_from_sectors_m2m",
                "set_satellites_snapshot_sector_list_from_sectors_m2m",
                "set_canteen_snapshot_epci_and_pat_list_from_city_insee_code",
            ],
            help="Command to run. Options are: 'set_canteen_id_before_v4', 'recreate_canteen_hard_deleted', 'set_canteen_snapshot_sector_list_from_sectors_m2m', 'set_satellites_snapshot_sector_list_from_sectors_m2m', 'set_canteen_snapshot_epci_and_pat_list_from_city_insee_code'",
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
        elif command == "set_canteen_snapshot_sector_list_from_sectors_m2m":
            self.set_canteen_snapshot_sector_list_from_sectors_m2m(apply)
        elif command == "set_satellites_snapshot_sector_list_from_sectors_m2m":
            self.set_satellites_snapshot_sector_list_from_sectors_m2m(apply)
        elif command == "set_canteen_snapshot_epci_and_pat_list_from_city_insee_code":
            self.set_canteen_snapshot_epci_and_pat_list_from_city_insee_code(apply)

    def set_canteen_id_before_v4(self, apply):
        diagnostic_updated_count = 0
        # teledeclaration_qs = Teledeclaration.objects.exclude(declared_data__version__gte=4)  # stored as string, harder...
        diagnostic_qs = (
            Diagnostic.objects.select_related("canteen").teledeclared().exclude(teledeclaration_version__gte=4)
        )
        print("Diagnostics teledeclared (with version < 4):", diagnostic_qs.count())
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
                                # save with change_reason
                                new_canteen.save()
                                update_change_reason(
                                    new_canteen,
                                    f"Script: recreate_canteen_hard_deleted (diagnostic_id {diagnostic.id})",
                                )
                                # M2M: sectors
                                for sector in canteen_satellite.get("sectors", []):
                                    new_canteen.sectors_m2m.add(sector["id"])
                            canteens_created_count += 1
                else:
                    print(f"Canteen satellite in Diagnostic {diagnostic.id} has no id, skipping")

        print("Done! Canteens recreated:", canteens_created_count)

    def set_canteen_snapshot_sector_list_from_sectors_m2m(self, apply):
        diagnostic_qs = Diagnostic.objects.teledeclared().filter(
            teledeclaration_version__gte=9, teledeclaration_version__lte=15
        )
        print("Diagnostics teledeclared (between v9 & v15):", diagnostic_qs.count())

        diagnostics_updated_count = 0
        for index, diagnostic in enumerate(diagnostic_qs):
            canteen_snapshot_temp = diagnostic.canteen_snapshot
            if canteen_snapshot_temp:
                sector_list_new = []
                if "sectors" in canteen_snapshot_temp:
                    sectors_old = canteen_snapshot_temp["sectors"]
                    sector_list_new = get_sector_list_from_old_sector_dict_list(sectors_old)
                if apply:
                    canteen_snapshot_temp["sector_list"] = sector_list_new
                    diagnostic.canteen_snapshot = canteen_snapshot_temp
                    diagnostic.save(update_fields=["canteen_snapshot"])
                    update_change_reason(diagnostic, "Script: set sector_list from sectors M2M")
                diagnostics_updated_count += 1
            if index % 5000 == 0:
                print(f"Processed {index} diagnostics out of {diagnostic_qs.count()}")

        print("Done! Diagnostics updated:", diagnostics_updated_count)

    def set_satellites_snapshot_sector_list_from_sectors_m2m(self, apply):
        diagnostic_qs = Diagnostic.objects.teledeclared().filter(
            teledeclaration_version__gte=9, teledeclaration_version__lte=15
        )
        print("Diagnostics teledeclared (between v9 & v15):", diagnostic_qs.count())

        diagnostics_updated_count = 0
        for index, diagnostic in enumerate(diagnostic_qs):
            satellites_snapshot_temp = diagnostic.satellites_snapshot
            if satellites_snapshot_temp:
                for satellite in satellites_snapshot_temp:
                    sector_list_new = []
                    if "sectors" in satellite:
                        sectors_old = satellite["sectors"]
                        sector_list_new = get_sector_list_from_old_sector_dict_list(sectors_old)
                    if apply:
                        satellite["sector_list"] = sector_list_new
                        diagnostic.satellites_snapshot = satellites_snapshot_temp
                        diagnostic.save(update_fields=["satellites_snapshot"])
                        update_change_reason(diagnostic, "Script: set satellite sector_list from sectors M2M")
                    diagnostics_updated_count += 1
            if index % 5000 == 0:
                print(f"Processed {index} diagnostics out of {diagnostic_qs.count()}")

        print("Done! Diagnostics updated:", diagnostics_updated_count)

    def set_canteen_snapshot_epci_and_pat_list_from_city_insee_code(self, apply):
        diagnostic_qs = Diagnostic.objects.teledeclared().filter(teledeclaration_version__lte=16)
        print("Diagnostics teledeclared (until v16 included):", diagnostic_qs.count())

        communes_details = map_communes_infos()
        pat_mapping = map_pat_list_to_communes_insee_code()

        diagnostics_updated_count = 0
        for index, diagnostic in enumerate(diagnostic_qs):
            canteen_snapshot_temp = diagnostic.canteen_snapshot
            if canteen_snapshot_temp:
                city_insee_code = canteen_snapshot_temp.get("city_insee_code")
                if city_insee_code:
                    # get epci & pat from city_insee_code
                    epci = communes_details.get(city_insee_code, {}).get("epci")
                    pat_list = pat_mapping.get(city_insee_code, [])
                    if apply:
                        canteen_snapshot_temp["epci"] = epci
                        canteen_snapshot_temp["pat_list"] = [pat["pat"] for pat in pat_list]
                        diagnostic.canteen_snapshot = canteen_snapshot_temp
                        diagnostic.save(update_fields=["canteen_snapshot"])
                        update_change_reason(diagnostic, "Script: set epci and pat_list from city_insee_code")
                    diagnostics_updated_count += 1
            if index % 5000 == 0:
                print(f"Processed {index} diagnostics out of {diagnostic_qs.count()}")

        print("Done! Diagnostics updated:", diagnostics_updated_count)
