import csv
import requests
import logging
from django.core.management.base import BaseCommand
from django.db import transaction, IntegrityError
from data.models import Canteen, Diagnostic, ManagerInvitation

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Creates models from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str, help="Path to csv file to import")
        return super().add_arguments(parser)

    def handle(self, *args, **options):
        print("Starting CSV import task")
        filepath = options["filepath"]
        print(f"Filepath to import : { filepath }")

        locations_csv_str = "siret,citycode\n"
        canteens_by_siret = {}

        with open(filepath, "r") as file:
            dialect = csv.Sniffer().sniff(file.read(1024))
            file.seek(0)
            reader = csv.reader(file, dialect)

            for row in reader:
                created_canteen = Command._create_models(row)
                if created_canteen:
                    canteens_by_siret[created_canteen.siret] = created_canteen
                    locations_csv_str += f"{created_canteen.siret},{created_canteen.city_insee_code}\n"

            Command._update_location_data(canteens_by_siret, locations_csv_str)
            logger.info(f"Successfully imported {len(canteens_by_siret)} canteens from CSV file {filepath}")

    @staticmethod
    def _create_models(row):
        if Command._is_header_row(row):
            print("Ingoring header row")
            return

        try:
            if not row[2]:
                logger.error(f"CSV row {row} does not contain a SIRET")
                return False

            siret = row[2].strip()

            if siret and Command._siret_exists(siret):
                logger.error(f"Canteen with SIRET {siret} exists already crating models from CSV row : {row}")
                return False

            name = row[3].strip()
            city_insee_code = row[4].strip()
            manager_email = row[7].strip() if row[7] else row[6].strip()
            production_type = Canteen.ProductionType.ON_SITE
            management_type = None

            try:
                daily_meal_count = int(row[13]) if row[13] else None
            except:
                daily_meal_count = None

            try:
                bio_and_sustainable_percentage = int(row[14]) if row[14] else None
            except:
                bio_and_sustainable_percentage = None

            try:
                bio_percentage = int(row[15]) if row[15] else None
            except:
                bio_percentage = None

            sustainable_percentage = None
            if bio_and_sustainable_percentage and bio_percentage:
                sustainable_percentage = bio_and_sustainable_percentage - bio_percentage

            if row[17] == "Oui":
                management_type = Canteen.ManagementType.DIRECT
            if row[18] == "Oui":
                management_type = Canteen.ManagementType.CONCEDED

            try:
                with transaction.atomic():
                    canteen = Canteen(
                        siret=siret,
                        name=name,
                        city_insee_code=city_insee_code,
                        production_type=production_type,
                        management_type=management_type,
                        daily_meal_count=daily_meal_count,
                        creation_campaign="Plan de soutien aux cantines scolaires des petites communes (CSV file)",
                    )
                    canteen.save()
                    diagnostic = None
                    if bio_percentage or sustainable_percentage:
                        diagnostic = Diagnostic(
                            value_bio_ht=bio_percentage,
                            value_sustainable_ht=sustainable_percentage,
                            canteen=canteen,
                            year=2021,
                        )
                        diagnostic.save()
                    manager_invitation = ManagerInvitation(
                        canteen=canteen,
                        email=manager_email,
                    )
                    manager_invitation.save()

                    logger.info(f"Created canteen {canteen.name} (ID: {canteen.id})")
                    logger.info(
                        f"Created manager invitaion for {manager_email} to join {canteen.name} (ID: {canteen.id})"
                    )
                    if diagnostic:
                        logger.info(f"Created diagnostic for 2021 for {canteen.name} (ID: {diagnostic.id})")
                    return canteen
            except IntegrityError as e:
                logger.error(f"Integrity error when crating models from CSV row : {row}")
                logger.exception(e)
                return False

        except Exception as e:
            logger.error(f"Unable to create cantine from CSV file : {row}")
            logger.exception(e)
            return False

    @staticmethod
    def _is_header_row(row):
        return row[1] == "Région Numéro Dossier"

    @staticmethod
    def _siret_exists(siret):
        try:
            Canteen.objects.get(siret=siret)
            return True
        except Canteen.DoesNotExist:
            return False

    @staticmethod
    def _update_location_data(canteens, locations_csv_str):
        try:
            # NB: max size of a csv file is 50 MB
            response = requests.post(
                "https://api-adresse.data.gouv.fr/search/csv/",
                files={
                    "data": ("locations.csv", locations_csv_str),
                },
                data={
                    "citycode": "citycode",
                    "result_columns": ["result_citycode", "result_postcode", "result_city", "result_context"],
                },
                timeout=100,
            )
            response.raise_for_status()  # Raise an exception if the request failed
            for row in csv.reader(response.text.splitlines()):
                if row[0] == "siret":
                    continue  # skip header
                if row[5] != "":  # city found, so rest of data is found
                    canteen = canteens[row[0]]
                    canteen.city_insee_code = row[2]
                    canteen.postal_code = row[3]
                    canteen.city = row[4]
                    canteen.department = row[5].split(",")[0]
                    canteen.save()
        except Exception as e:
            logger.error(f"Error while updating location data : {repr(e)} - {e}")
