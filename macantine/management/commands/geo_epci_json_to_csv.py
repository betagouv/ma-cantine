import csv

from django.core.management.base import BaseCommand

from common.api.decoupage_administratif import fetch_epcis

EPCI_CSV_FILE = "macantine/geo/epcis.csv"
EPCI_CSV_HEADER = ["code", "nom", "departements", "regions", "population"]


class Command(BaseCommand):
    help = "Fetch the list of EPCI from the API and save it to a CSV file in the geo folder"

    def handle(self, *args, **options):
        # Etape 1: récupérer les données, stats
        with open(EPCI_CSV_FILE, "r", encoding="utf-8") as csvfile:
            self.stdout.write(f"{EPCI_CSV_FILE} contains {sum(1 for _ in csvfile) - 1} EPCIs.")
        epcis_json = fetch_epcis()
        self.stdout.write(f"The API returned {len(epcis_json)} EPCIs.")

        # Etape 2: mettre à jour le fichier CSV
        with open(EPCI_CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=EPCI_CSV_HEADER)
            writer.writeheader()
            for epci in epcis_json:
                writer.writerow(
                    {
                        "code": epci["code"],
                        "nom": epci["nom"],
                        "departements": ",".join(epci["codesDepartements"]),
                        "regions": ",".join(epci["codesRegions"]),
                        "population": epci["population"],
                    }
                )

        # Done !
        self.stdout.write(f"{EPCI_CSV_FILE} was updated successfully!")
