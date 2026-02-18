import difflib
import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from data.models import Diagnostic

GITHUB_REPO_URL = "https://github.com/betagouv/ma-cantine"
GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/main"

COMMON_FIELDS = {
    "siret": {
        "constraints": {"required": True, "unique": True},
        "description": "L'établissement avec ce SIRET doit être déjà enregistré sur notre plateforme.",
        "example": "49463556926130",
        "format": "default",
        "name": "siret",
        "title": "SIRET de l'établissement",
        "type": "any",
    },
    "année_bilan": {
        "constraints": {"required": True},
        "description": "Réfère à l'année des données et non l'année de déclaration.",
        "example": "2021",
        "name": "année_bilan",
        "title": "Année du bilan",
        "type": "any",
    },
}

SCHEMA_SPECS = {
    "simple": {
        "file_name": "bilans_simple.json",
        "fields": Diagnostic.SIMPLE_APPRO_FIELDS,
        "required": Diagnostic.SIMPLE_APPRO_FIELDS_REQUIRED_2025,
        "schema_name": "import-bilans-simple",
        "schema_title": "Schema import des bilans (simple)",
    },
    "detaille": {
        "file_name": "bilans_detaille.json",
        "fields": Diagnostic.COMPLETE_APPRO_FIELDS,
        "required": Diagnostic.COMPLETE_APPRO_FIELDS_REQUIRED_2025,
        "schema_name": "import-bilans-detaille",
        "schema_title": "Schema import des bilans (detaille)",
    },
}


class Command(BaseCommand):
    """
    Exemples:
    - python manage.py generate_import_schema --schema detaille --show-diff
    - python manage.py generate_import_schema --schema detaille --dry-run
    """

    help = "Regenerate bilan import schema JSON files from Diagnostic fields."

    def add_arguments(self, parser):
        parser.add_argument(
            "--schema",
            choices=sorted(SCHEMA_SPECS.keys()),
            required=True,
            help="Regenerate only the selected schema.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show which files would change without writing them.",
        )
        parser.add_argument(
            "--show-diff",
            action="store_true",
            help="Print a unified diff without writing files.",
        )

    def handle(self, *args, **options):
        selected_schema = options.get("schema")
        show_diff = options.get("show_diff")
        dry_run = options.get("dry_run") or show_diff

        for schema_key, spec in SCHEMA_SPECS.items():
            if schema_key != selected_schema:
                continue
            schema_path = self._schema_path(spec["file_name"])
            old_schema = self._read_schema_text(schema_path)
            new_schema = self._build_schema(spec)
            new_schema_json = json.dumps(new_schema, ensure_ascii=False, indent=2, sort_keys=True)

            schema_changed = old_schema != new_schema_json
            if schema_changed:
                if show_diff:
                    self._print_schema_diff(schema_path, old_schema, new_schema_json)
                elif not dry_run:
                    self._write_schema_text(schema_path, new_schema_json)
                    self.stdout.write(self.style.SUCCESS(f"Updated schema file: {schema_path}"))
            else:
                self.stdout.write(f"No changes for schema file: {schema_path}")

    def _schema_path(self, file_name: str) -> Path:
        return Path(settings.BASE_DIR) / "data" / "schemas" / "imports" / file_name

    def _build_schema(self, spec: dict) -> dict:
        schema = {
            "encoding": "utf-8",
            "fields": [],
            "homepage": GITHUB_REPO_URL,
            "name": spec["schema_name"],
            "path": f"{GITHUB_RAW_BASE_URL}/data/schemas/imports/{spec['file_name']}",
            "title": spec["schema_title"],
        }
        required_names = {"siret", "année_bilan", *spec["required"]}
        ordered_names = ["siret", "année_bilan", *spec["fields"]]

        for name in ordered_names:
            field = self._build_field_definition(name)
            self._set_required(field, name in required_names)
            schema["fields"].append(field)

        return schema

    def _build_field_definition(self, name: str) -> dict:
        if name in COMMON_FIELDS.keys():
            return COMMON_FIELDS[name]

        title = name
        try:
            model_field = Diagnostic._meta.get_field(name)
            title = str(model_field.verbose_name)
        except Exception:
            pass

        return {
            "description": "",
            "example": "1234.99",
            "name": name,
            "title": title,
            "type": "number",
        }

    def _set_required(self, field: dict, is_required: bool) -> None:
        constraints = dict(field.get("constraints") or {})
        if is_required:
            constraints["required"] = True
        else:
            constraints.pop("required", None)

        if constraints:
            field["constraints"] = constraints
        else:
            field.pop("constraints", None)

    def _read_schema_text(self, schema_path: Path) -> str:
        if schema_path.exists():
            return schema_path.read_text(encoding="utf-8").strip()
        return ""

    def _write_schema_text(self, schema_path: Path, content: str) -> None:
        schema_path.write_text(f"{content}\n", encoding="utf-8")

    def _print_schema_diff(self, schema_path: Path, old_json: str, new_json: str) -> None:
        diff_lines = difflib.unified_diff(
            old_json.splitlines(),
            new_json.splitlines(),
            fromfile=str(schema_path),
            tofile=str(schema_path),
            lineterm="",
        )
        self.stdout.write("\n".join(diff_lines))
