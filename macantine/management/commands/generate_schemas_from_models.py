import json

from django.core.management.base import BaseCommand

from data.models import Purchase

IMPORT_SCHEMAS_FOLDER_PATH = "data/schemas/imports"
SCHEMA_SQUELETON = {
    "$schema": "https://frictionlessdata.io/schemas/table-schema.json",
    "encoding": "utf-8",
    "fields": [],
    "homepage": "",
    "name": "",
    "path": "",
    "title": "",
}


class Command(BaseCommand):
    help = "Générer les schémas d'import de données à partir des modèles Django"

    def handle(self, *args, **options):
        schema = SCHEMA_SQUELETON.copy()

        for field in Purchase._meta.fields:
            field_schema = {
                "name": field.name,
                "title": field.verbose_name,
                "description": field.help_text,
                "type": field.get_internal_type(),  # TODO: mapping
                "format": "default",  # TODO: mapping
                "example": "",  # TODO
                "constraints": {},  # see below
            }
            # constraints
            if field.choices:
                field_choice_list = [choice[0] for choice in field.choices]
                field_schema["constraints"]["enum"] = field_choice_list
                field_schema["doc_enum"] = field_choice_list
                # doc_enum_multiple, doc_enum_multiple_seperator
            # return
            schema["fields"].append(field_schema)

        with open(IMPORT_SCHEMAS_FOLDER_PATH + "/purchase.json", "w") as f:
            json.dump(schema, f, ensure_ascii=True, indent=2)
