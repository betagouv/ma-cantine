import json
import mimetypes
import re
from pathlib import Path

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

VALIDATA_PROD_API_URL = "https://api.validata.etalab.studio/validate"

TESTS_DIR = Path(settings.BASE_DIR) / "api/tests"
FILES_DIR = TESTS_DIR / "files"
SCHEMAS_BASE_URL = f"{settings.GITHUB_RAW_BASE_URL}/data/schemas/imports"

# Maps each (test file, category) pair to the schema its imports are validated against.
# `category` is the mock_validata_response(mock, filename, category=...) argument, which is
# also the api/tests/files/ subdirectory the fixture (and its source CSV/XLSX) lives in.
# Most test files only ever validate against one schema, so their calls omit `category` and
# fall back to its default ("canteens"). Test files that exercise more than one schema (e.g.
# diagnostics-simple import by SIRET vs by id) pass `category` explicitly per call to pick
# the right one below.
SCHEMA_URLS = {
    ("test_canteens_create_import.py", "canteens"): f"{SCHEMAS_BASE_URL}/cantines_creer.json",
    ("test_canteens_update_import.py", "canteens"): f"{SCHEMAS_BASE_URL}/cantines_modifier.json",
    ("test_canteens_managers_import.py", "canteen_managers"): f"{SCHEMAS_BASE_URL}/cantines_gestionnaires.json",
    ("test_purchases_import.py", "achats"): f"{SCHEMAS_BASE_URL}/achats_siret.json",
    ("test_purchases_import.py", "achats_id"): f"{SCHEMAS_BASE_URL}/achats_id.json",
    ("test_purchases_import_old.py", "achats"): f"{SCHEMAS_BASE_URL}/achats_siret_old.json",
    ("test_purchases_import_old.py", "achats_id"): f"{SCHEMAS_BASE_URL}/achats_id_old.json",
    ("test_diagnostics_complete_import.py", "diagnostics_complete"): f"{SCHEMAS_BASE_URL}/bilans_detaille.json",
    ("test_diagnostics_simple_import.py", "diagnostics_simple"): f"{SCHEMAS_BASE_URL}/bilans_simple_siret.json",
    ("test_diagnostics_simple_import.py", "diagnostics"): f"{SCHEMAS_BASE_URL}/bilans_simple_id.json",
}

# Some categories don't have their own api/tests/files/ subdirectory: their source CSV/XLSX
# fixtures physically live alongside another category's (only the schema differs), so their
# captured Validata responses are cached separately under their own category name, but read
# their source file from this directory instead.
SOURCE_DIR_OVERRIDES = {
    "achats_id": "achats",
}

MOCK_CALL_RE = re.compile(r'mock_validata_response\(\s*mock,\s*"([^"]+)"(?:,\s*category="([^"]+)")?,?\s*\)')


class Command(BaseCommand):
    """
    Exemples:
    - python manage.py generate_validata_test_fixtures
    - python manage.py generate_validata_test_fixtures canteens_good.csv canteens_bad.csv
    """

    help = (
        "Regenerate the captured Validata API responses used to mock canteen/purchase/diagnostic "
        "import tests (see api/tests/files/<category>/validata_responses/README.md). Calls the "
        "real, live Validata API, so it requires internet access."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "filenames",
            nargs="*",
            help=(
                "Specific fixture filenames to regenerate (e.g. canteens_good.csv). "
                "Defaults to every file referenced via mock_validata_response(mock, ...) "
                "in the canteen/purchase/diagnostic import tests."
            ),
        )

    def handle(self, *args, **options):
        targets = self._discover_targets()

        if options["filenames"]:
            wanted = set(options["filenames"])
            found = {filename for _, filename in targets}
            missing = wanted - found
            if missing:
                self.stderr.write(
                    f"Not referenced by mock_validata_response(...) in any test, skipping: {', '.join(sorted(missing))}"
                )
            targets = {
                (category, filename): url for (category, filename), url in targets.items() if filename in wanted
            }

        for (category, filename), schema_url in sorted(targets.items()):
            self._capture(category, filename, schema_url)

    def _discover_targets(self) -> dict:
        targets = {}
        for (test_file, category), schema_url in SCHEMA_URLS.items():
            content = (TESTS_DIR / test_file).read_text()
            for filename, explicit_category in MOCK_CALL_RE.findall(content):
                if (explicit_category or "canteens") == category:
                    targets[(category, filename)] = schema_url
        return targets

    def _capture(self, category, filename, schema_url):
        source_dir = FILES_DIR / SOURCE_DIR_OVERRIDES.get(category, category)
        file_path = source_dir / filename
        if not file_path.exists():
            self.stderr.write(f"{category}/{filename}: source file not found at {file_path}, skipping")
            return

        content_type = mimetypes.guess_type(filename)[0] or "text/csv"
        with open(file_path, "rb") as f:
            response = requests.post(
                VALIDATA_PROD_API_URL,
                files={"file": (filename, f.read(), content_type)},
                data={"schema": schema_url, "ignore_header_case": True, "include_resource_data": True},
            )
        data = response.json()
        # Strip fields that vary between calls but aren't used by the app, so that
        # regenerating without an actual content/schema change produces an empty diff.
        data["date"] = None
        if "report" in data:
            data["report"]["stats"]["seconds"] = None

        responses_dir = FILES_DIR / category / "validata_responses"
        responses_dir.mkdir(parents=True, exist_ok=True)
        out_path = responses_dir / f"{filename}.json"
        with open(out_path, "w") as out:
            json.dump(data, out, indent=2, ensure_ascii=False)
            out.write("\n")

        error_count = len(data.get("report", {}).get("errors", [])) if "report" in data else "N/A (top-level error)"
        self.stdout.write(f"{category}/{filename}: status={response.status_code} errors={error_count} -> {out_path}")
