import csv
import logging
import time
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count

from common.api.recherche_entreprises import fetch_geo_data_from_siret
from data.models import Canteen
from data.utils import read_csv

logger = logging.getLogger(__name__)

DEFAULT_SLEEP_SECONDS = 0.25


class Command(BaseCommand):
    """
    Export Recherche Entreprises geodata for canteen SIRETs to a local CSV cache.

    Usage:
    - uv run python manage.py canteen_siret_recherche_entreprises_cache_csv --output stats/recherche_entreprises_cache.csv
    - uv run python manage.py canteen_siret_recherche_entreprises_cache_csv --output stats/recherche_entreprises_cache.csv --resume
    - uv run python manage.py canteen_siret_recherche_entreprises_cache_csv --output stats/recherche_entreprises_cache.csv --retry-errors
    """

    help = "Export a reusable CSV cache of Recherche Entreprises responses for canteen SIRETs"

    CSV_HEADERS = [
        "siret",
        "canteen_count",
        "status",
        "name",
        "city_insee_code",
        "postal_code",
        "city",
        "epci",
        "department",
        "region",
        "etat_administratif",
        "date_fermeture",
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            dest="output",
            type=str,
            required=True,
            help="CSV output path",
        )
        parser.add_argument(
            "--resume",
            action="store_true",
            dest="resume",
            help="Append to existing CSV and skip SIRETs already present in it.",
        )
        parser.add_argument(
            "--retry-errors",
            action="store_true",
            dest="retry_errors",
            help="Read --output CSV, find all rows with status=error, re-fetch them, and update --output in-place.",
        )

    def handle(self, *args, **options):
        output_path = Path(options["output"])
        resume = options["resume"]
        retry_errors = options.get("retry_errors", False)

        if retry_errors:
            self._handle_retry_errors(output_path)
            return

        output_path.parent.mkdir(parents=True, exist_ok=True)

        cached_sirets = set()
        existing_rows = []
        if resume and output_path.exists():
            existing_rows = read_csv(output_path)
            cached_sirets = self._read_existing_sirets(output_path)
            logger.info("Resume mode: loaded %s cached SIRETs from %s", len(cached_sirets), output_path)

        base_qs = Canteen.all_objects.has_siret().values("siret").annotate(canteen_count=Count("id")).order_by("siret")
        if cached_sirets:
            base_qs = base_qs.exclude(siret__in=cached_sirets)

        total_to_process = base_qs.count()
        logger.info("Start task: canteen_siret_recherche_entreprises_cache_csv")
        logger.info("SIRETs to fetch: %s", total_to_process)

        if total_to_process == 0:
            if resume and output_path.exists():
                sorted_rows = self._sort_rows_by_siret(existing_rows)
                self._write_rows_to_csv(output_path, sorted_rows)
                logger.info("No new SIRETs. Existing CSV re-sorted by SIRET at %s", output_path)
            logger.info("Nothing to do.")
            return

        stats = {
            "ok": 0,
            "not_found": 0,
            "error": 0,
            "api_calls": 0,
        }

        new_rows = []
        for index, row in enumerate(base_qs.iterator(), start=1):
            siret = row["siret"]
            canteen_count = row["canteen_count"]

            api_response, status = self._fetch_and_track_status(siret, stats)
            csv_row = self._build_csv_row(siret, canteen_count, api_response, status)
            new_rows.append(csv_row)

            if index % 1000 == 0:
                logger.info("Progress: %s/%s", index, total_to_process)

            time.sleep(DEFAULT_SLEEP_SECONDS)

        rows_to_write = new_rows
        if resume and output_path.exists():
            rows_by_siret = {row.get("siret"): row for row in existing_rows if row.get("siret")}
            rows_by_siret.update({row["siret"]: row for row in new_rows})
            rows_to_write = self._sort_rows_by_siret(rows_by_siret.values())

        self._write_rows_to_csv(output_path, rows_to_write)

        logger.info("CSV written to %s", output_path)
        logger.info("API calls: %s", stats["api_calls"])
        logger.info("Status OK: %s", stats["ok"])
        logger.info("Status not_found: %s", stats["not_found"])
        logger.info("Status error: %s", stats["error"])
        logger.info("End task: canteen_siret_recherche_entreprises_cache_csv")

    @staticmethod
    def _read_existing_sirets(output_path):
        rows = read_csv(output_path)
        return {row.get("siret") for row in rows if row.get("siret")}

    def _handle_retry_errors(self, csv_path):
        """
        Read CSV, extract all rows with status=error, re-fetch those SIRETs,
        and update rows in-place to preserve original SIRET ordering.
        """
        if not csv_path.exists():
            raise CommandError(f"CSV file not found: {csv_path}")

        logger.info("Start task: retry_errors on %s", csv_path)

        # Read all rows from CSV
        all_rows = read_csv(csv_path)
        error_indices = {index: row for index, row in enumerate(all_rows) if row.get("status") == "error"}

        logger.info("Found %s rows with status=error to retry", len(error_indices))

        if not error_indices:
            logger.info("No error rows to retry. Nothing to do.")
            return

        stats = {"ok": 0, "not_found": 0, "error": 0, "api_calls": 0}

        for seq_index, (row_index, original_row) in enumerate(error_indices.items(), start=1):
            siret = original_row["siret"]
            canteen_count = original_row.get("canteen_count", 1)
            api_response, status = self._fetch_and_track_status(siret, stats)

            # Update row in-place
            all_rows[row_index] = self._build_csv_row(siret, canteen_count, api_response, status)

            if seq_index % 100 == 0:
                logger.info("Progress: %s/%s", seq_index, len(error_indices))

            time.sleep(DEFAULT_SLEEP_SECONDS)

        # Write all rows back to CSV in original order
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.CSV_HEADERS)
            writer.writeheader()
            for row in all_rows:
                writer.writerow(row)

        logger.info("CSV updated at %s", csv_path)
        logger.info("Retried API calls: %s", stats["api_calls"])
        logger.info("Status OK: %s", stats["ok"])
        logger.info("Status not_found: %s", stats["not_found"])
        logger.info("Status error: %s", stats["error"])
        logger.info("End task: retry_errors")

    @staticmethod
    def _get_response_status(api_response):
        if not api_response:
            return "not_found"
        if api_response.get("city_insee_code"):
            return "ok"
        return "error"

    def _fetch_and_track_status(self, siret, stats):
        api_response = fetch_geo_data_from_siret(siret)
        status = self._get_response_status(api_response)
        stats[status] += 1
        stats["api_calls"] += 1
        return api_response, status

    @staticmethod
    def _build_csv_row(siret, canteen_count, api_response, status):
        return {
            "siret": siret,
            "canteen_count": canteen_count,
            "status": status,
            "name": api_response.get("name") if api_response else None,
            "city_insee_code": api_response.get("city_insee_code") if api_response else None,
            "postal_code": api_response.get("postal_code") if api_response else None,
            "city": api_response.get("city") if api_response else None,
            "epci": api_response.get("epci") if api_response else None,
            "department": api_response.get("department") if api_response else None,
            "region": api_response.get("region") if api_response else None,
            "etat_administratif": api_response.get("etat_administratif") if api_response else None,
            "date_fermeture": api_response.get("date_fermeture") if api_response else None,
        }

    def _write_rows_to_csv(self, output_path, rows):
        with output_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.CSV_HEADERS)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    @staticmethod
    def _sort_rows_by_siret(rows):
        return sorted(rows, key=lambda row: row.get("siret") or "")
