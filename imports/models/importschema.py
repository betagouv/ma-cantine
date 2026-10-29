from functools import cached_property

from django.conf import settings

from common.utils import file_import

SCHEMAS_FOLDER_PATH = "data/schemas/imports"


class ImportSchema:
    """
    A JSON Table Schema accepted by an import (stored in data/schemas/imports/)
    """

    def __init__(self, file_name):
        self.name = file_name

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
