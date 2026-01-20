import json

from django.core.management.base import BaseCommand

from common.api.datagouv import fetch_pats
from common.api.decoupage_administratif import fetch_communes, fetch_departements, fetch_epcis, fetch_regions


class Command(BaseCommand):
    help = "Generate geo data to JSON file for a specific scope"

    def add_arguments(self, parser):
        parser.add_argument(
            "--scope",
            dest="scope",
            type=str,
            choices=["region", "department", "pat", "epci", "city"],
            required=True,
            help="Scope of the geo data to generate (region, department, pat, epci, city)",
        )

    def handle(self, *args, **options):
        scope = options["scope"]

        # TODO: order by name?
        # TODO: add timestamp in filename?

        if scope == "region":
            region_list = fetch_regions()
            # no need to filter, already contains only the code and name
            # TODO: order by name
            # export to JSON file
            with open(f"{scope}.json", "w", encoding="utf-8") as f:
                json.dump(region_list, f, ensure_ascii=False, indent=4)

        elif scope == "department":
            department_list = fetch_departements()
            department_list_filtered = [
                {
                    "code": department["code"],
                    "nom": department["nom"],
                    # "codeRegion": department["codeRegion"],
                }
                for department in department_list
            ]
            # export to JSON file
            with open(f"{scope}.json", "w", encoding="utf-8") as f:
                json.dump(department_list_filtered, f, ensure_ascii=False, indent=4)

        elif scope == "pat":
            pat_list = fetch_pats()
            pat_list_filtered = [
                {
                    "code": pat["id"],
                    "nom": pat["nom_administratif"],
                }
                for pat in pat_list
            ]
            # export to JSON file
            with open(f"{scope}.json", "w", encoding="utf-8") as f:
                json.dump(pat_list_filtered, f, ensure_ascii=False, indent=4)

        elif scope == "epci":
            epci_list = fetch_epcis()
            # no need to filter, already contains only the code and name
            # export to JSON file
            with open("epci.json", "w", encoding="utf-8") as f:
                json.dump(epci_list, f, ensure_ascii=False, indent=4)

        elif scope == "city":
            city_list = fetch_communes()
            city_list_filtered = [
                {
                    "code": city["code"],
                    "nom": city["nom"],
                    "codeDepartement": city["codeDepartement"],
                    # "codeRegion": city["codeRegion"],
                }
                for city in city_list
            ]
            # export to JSON file
            with open(f"{scope}.json", "w", encoding="utf-8") as f:
                json.dump(city_list_filtered, f, ensure_ascii=False, indent=4)

        self.stdout.write(self.style.SUCCESS(f"Geo data for {scope} has been generated successfully."))
