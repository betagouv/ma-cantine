import json
import mimetypes
import re
from pathlib import Path

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

VALIDATA_PROD_API_URL = "https://api.validata.etalab.studio/validate"

FILES_DIR = Path(settings.BASE_DIR) / "api/tests/files/canteens"
RESPONSES_DIR = FILES_DIR / "validata_responses"

# Maps each test file to the schema its imports are validated against.
SCHEMA_URLS = {
    Path(settings.BASE_DIR)
    / "api/tests/test_canteens_create_import.py": f"{settings.GITHUB_RAW_BASE_URL}/data/schemas/imports/cantines_creer.json",
    Path(settings.BASE_DIR)
    / "api/tests/test_canteens_update_import.py": f"{settings.GITHUB_RAW_BASE_URL}/data/schemas/imports/cantines_modifier.json",
}

MOCK_CALL_RE = re.compile(r'mock_validata_response\(mock,\s*"([^"]+)"\)')


class Command(BaseCommand):
    """
    Exemples:
    - python manage.py generate_validata_test_fixtures
    - python manage.py generate_validata_test_fixtures canteens_good.csv canteens_bad.csv
    """

    help = (
        "Regenerate the captured Validata API responses used to mock canteen import tests "
        "(see api/tests/files/canteens/validata_responses/README.md). Calls the real, live "
        "Validata API, so it requires internet access."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "filenames",
            nargs="*",
            help=(
                "Specific fixture filenames to regenerate (e.g. canteens_good.csv). "
                "Defaults to every file referenced via mock_validata_response(mock, ...) "
                "in the canteen create/update import tests."
            ),
        )

    def handle(self, *args, **options):
        targets = self._discover_targets()

        if options["filenames"]:
            wanted = set(options["filenames"])
            missing = wanted - targets.keys()
            if missing:
                self.stderr.write(
                    f"Not referenced by mock_validata_response(...) in any test, skipping: {', '.join(sorted(missing))}"
                )
            targets = {name: url for name, url in targets.items() if name in wanted}

        RESPONSES_DIR.mkdir(exist_ok=True)
        for filename, schema_url in sorted(targets.items()):
            self._capture(filename, schema_url)

    def _discover_targets(self) -> dict:
        targets = {}
        for test_file, schema_url in SCHEMA_URLS.items():
            for filename in MOCK_CALL_RE.findall(test_file.read_text()):
                targets[filename] = schema_url
        return targets

    def _capture(self, filename, schema_url):
        file_path = FILES_DIR / filename
        if not file_path.exists():
            self.stderr.write(f"{filename}: source file not found at {file_path}, skipping")
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

        out_path = RESPONSES_DIR / f"{filename}.json"
        with open(out_path, "w") as out:
            json.dump(data, out, indent=2, ensure_ascii=False)
            out.write("\n")

        error_count = len(data.get("report", {}).get("errors", [])) if "report" in data else "N/A (top-level error)"
        self.stdout.write(f"{filename}: status={response.status_code} errors={error_count} -> {out_path}")
