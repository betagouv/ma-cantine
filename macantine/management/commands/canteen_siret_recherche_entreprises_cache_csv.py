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
BATCH_WRITE_EVERY = 100

CSV_HEADERS = [
    "siret",
    "canteen_count",
    "status",
    "name",
    "city_insee_code",
    "postal_code",
    "city",
    "address",
    "latitude",
    "longitude",
    "epci",
    "department",
    "region",
    "etat_administratif",
    "date_creation",
    "date_debut_activite",
    "date_fermeture",
    "activite_principale",
    "activite_principale_naf25",
]


class Command(BaseCommand):
    """
    Export Recherche Entreprises geodata for canteen SIRETs to a local CSV cache.

    Usage:
    - uv run python manage.py canteen_siret_recherche_entreprises_cache_csv --output stats/recherche_entreprises_cache.csv
    - uv run python manage.py canteen_siret_recherche_entreprises_cache_csv --output stats/recherche_entreprises_cache.csv --resume
    - uv run python manage.py canteen_siret_recherche_entreprises_cache_csv --output stats/recherche_entreprises_cache.csv --retry-errors
    """

    help = "Export a reusable CSV cache of Recherche Entreprises responses for canteen SIRETs"

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
        if resume and output_path.exists():
            cached_sirets = self._read_existing_sirets(output_path)
            logger.info("Resume mode: loaded %s cached SIRETs from %s", len(cached_sirets), output_path)

        base_qs = Canteen.all_objects.has_siret().values("siret").annotate(canteen_count=Count("id")).order_by("siret")
        if cached_sirets:
            base_qs = base_qs.exclude(siret__in=cached_sirets)

        total_to_process = base_qs.count()
        logger.info("Start task: canteen_siret_recherche_entreprises_cache_csv")
        logger.info("SIRETs to fetch: %s", total_to_process)

        if total_to_process == 0:
            logger.info("Nothing to do.")
            return

        stats = {
            "ok": 0,
            "not_found": 0,
            "error": 0,
            "api_calls": 0,
        }

        file_exists = output_path.exists()
        write_mode = "a" if resume and file_exists else "w"
        should_write_header = write_mode == "w" or output_path.stat().st_size == 0

        with output_path.open(write_mode, newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
            if should_write_header:
                writer.writeheader()

            batch_rows = []
            for index, row in enumerate(base_qs.iterator(), start=1):
                siret = row["siret"]
                canteen_count = row["canteen_count"]

                api_response, status = self._fetch_and_track_status(siret, stats)
                csv_row = self._build_csv_row(siret, canteen_count, api_response, status)
                batch_rows.append(csv_row)

                if len(batch_rows) == BATCH_WRITE_EVERY:
                    writer.writerows(batch_rows)
                    csv_file.flush()
                    batch_rows = []

                if index % 1000 == 0:
                    logger.info("Progress: %s/%s", index, total_to_process)

                time.sleep(DEFAULT_SLEEP_SECONDS)

            if batch_rows:
                writer.writerows(batch_rows)
                csv_file.flush()

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
        updated_since_last_write = 0

        for seq_index, (row_index, original_row) in enumerate(error_indices.items(), start=1):
            siret = original_row["siret"]
            canteen_count = original_row.get("canteen_count", 1)
            api_response, status = self._fetch_and_track_status(siret, stats)

            # Update row in-place
            all_rows[row_index] = self._build_csv_row(siret, canteen_count, api_response, status)
            updated_since_last_write += 1

            if updated_since_last_write == BATCH_WRITE_EVERY:
                self._write_rows_to_csv(csv_path, all_rows)
                logger.info("Progress: %s/%s (checkpoint saved)", seq_index, len(error_indices))
                updated_since_last_write = 0

            if seq_index % 100 == 0:
                logger.info("Progress: %s/%s", seq_index, len(error_indices))

            time.sleep(DEFAULT_SLEEP_SECONDS)

        # Final write to persist remaining updates in original order
        self._write_rows_to_csv(csv_path, all_rows)

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
        base = {
            "siret": siret,
            "canteen_count": canteen_count,
            "status": status,
        }
        response_data = {
            field: (api_response.get(field) if api_response else None) for field in CSV_HEADERS if field not in base
        }
        return {
            **base,
            **response_data,
        }

    def _write_rows_to_csv(self, output_path, rows):
        with output_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    @staticmethod
    def _sort_rows_by_siret(rows):
        return sorted(rows, key=lambda row: row.get("siret") or "")
