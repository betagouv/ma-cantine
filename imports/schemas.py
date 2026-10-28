from functools import cached_property

from django.conf import settings

from common.utils import file_import

SCHEMAS_FOLDER_PATH = "data/schemas/imports"


class ImportSchema:
    """
    A JSON Table Schema accepted by an import (stored in data/schemas/imports/)

    - import_type: ImportType to log (if the import accepts schemas of different types)
    """

    def __init__(self, file_name, import_type=None):
        self.name = file_name
        self.import_type = import_type

    def __repr__(self):
        return f"ImportSchema({self.name})"

    @property
    def path(self):
        return f"{SCHEMAS_FOLDER_PATH}/{self.name}"

    @property
    def url(self):
        # Validata fetches the schema from GitHub
        return f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{self.path}"

    @cached_property
    def header(self):
        return file_import.get_expected_header_from_schema(self.path)


def detect_schema(file_header, schemas):
    """Return the schema whose header matches exactly the file header (None if no match)"""
    return next((schema for schema in schemas if schema.header == file_header), None)
