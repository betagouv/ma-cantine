import difflib
import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from common.api import validata
from data.models import Diagnostic

COMMON_FIELDS = {
    "cantine_id": {
        "constraints": {"required": True, "unique": True},
        "description": "",
        "example": "949",
        "format": "default",
        "name": "cantine_id",
        "title": "Numéro ID de l'établissement pour lequel créer ou modifier le bilan",
        "type": "number",
    },
    "siret": {
        "constraints": {"required": True, "unique": True},
        "description": "L'établissement avec ce SIRET doit être déjà enregistré sur notre plateforme",
        "example": "49463556926130",
        "format": "default",
        "name": "siret",
        "title": "SIRET de l'établissement",
        "type": "any",
    },
    "année_bilan": {
        "constraints": {"required": True},
        "description": "Réfère à l'année des données et non l'année de déclaration",
        "example": "2021",
        "name": "année_bilan",
        "title": "Année du bilan",
        "type": "any",
    },
}

SCHEMA_SPECS = {
    "Diagnostic": {
        "simple_id": {
            "file_name": "bilans_simple_id.json",
            "fields_ordered": ["cantine_id", "année_bilan"] + Diagnostic.SIMPLE_APPRO_FIELDS,
            "fields_required": ["cantine_id", "année_bilan"] + Diagnostic.SIMPLE_APPRO_FIELDS_REQUIRED_2025,
            "schema_name": "import-bilans-simple-id",
            "schema_title": "Schema import des bilans (simple) par ID",
        },
        "simple_siret": {
            "file_name": "bilans_simple_siret.json",
            "fields_ordered": ["siret", "année_bilan"] + Diagnostic.SIMPLE_APPRO_FIELDS,
            "fields_required": ["siret", "année_bilan"] + Diagnostic.SIMPLE_APPRO_FIELDS_REQUIRED_2025,
            "schema_name": "import-bilans-simple-siret",
            "schema_title": "Schema import des bilans (simple) par SIRET",
        },
        "detaille": {
            "file_name": "bilans_detaille.json",
            "fields_ordered": ["siret", "année_bilan"] + Diagnostic.COMPLETE_APPRO_FIELDS,
            "fields_required": ["siret", "année_bilan"] + Diagnostic.COMPLETE_APPRO_FIELDS_REQUIRED_2025,
            "schema_name": "import-bilans-detaille",
            "schema_title": "Schema import des bilans (detaille)",
        },
    },
}


class Command(BaseCommand):
    """
    Exemples:
    - python manage.py generate_import_schema --model Diagnostic --schema detaille --show-diff
    - python manage.py generate_import_schema --model Diagnostic --schema detaille --dry-run
    """

    help = "Regenerate import schema JSON files from model fields."

    def add_arguments(self, parser):
        parser.add_argument(
            "--model",
            choices=sorted(SCHEMA_SPECS.keys()),
            required=True,
            help="Select the model for which to regenerate import schemas.",
        )
        parser.add_argument(
            "--schema",
            choices=sorted(
                {schema_key for model_schemas in SCHEMA_SPECS.values() for schema_key in model_schemas.keys()}
            ),
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
        model = options.get("model")
        model_schema = options.get("schema")
        show_diff = options.get("show_diff")
        dry_run = options.get("dry_run") or show_diff

        schema_spec = SCHEMA_SPECS.get(model, {}).get(model_schema)
        if not schema_spec:
            self.stdout.write(
                self.style.ERROR(f"No schema specification found for model '{model}' and schema '{model_schema}'")
            )
            return

        schema_path = self._schema_path(schema_spec["file_name"])
        old_schema = self._read_schema_text(schema_path)
        new_schema = self._build_schema(schema_spec)
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

    def _build_schema(self, schema_spec: dict) -> dict:
        schema = {
            "$schema": validata.FRICTIONLESS_SCHEMA_URL,
            "encoding": "utf-8",
            "fields": [],
            "homepage": settings.GITHUB_REPO_URL,
            "name": schema_spec["schema_name"],
            "path": f"{settings.GITHUB_RAW_BASE_URL}/data/schemas/imports/{schema_spec['file_name']}",
            "title": schema_spec["schema_title"],
        }

        for name in schema_spec["fields_ordered"]:
            field = self._build_field_definition(name, is_required=name in schema_spec["fields_required"])
            schema["fields"].append(field)

        return schema

    def _build_field_definition(self, name: str, is_required=False) -> dict:
        if name in COMMON_FIELDS.keys():
            return COMMON_FIELDS[name]

        title = name
        try:
            model_field = Diagnostic._meta.get_field(name)
            title = str(model_field.verbose_name)
        except Exception:
            pass

        field_definition = {
            "description": "",
            "example": "1234.99",
            "name": name,
            "title": title,
            "type": "number",
        }

        if is_required:
            field_definition["constraints"] = {"required": True}

        return field_definition

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
