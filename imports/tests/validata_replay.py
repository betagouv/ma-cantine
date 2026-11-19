"""
Replay the Validata API responses in the import tests (instead of calling the live API at each test run)

The responses are recorded in imports/tests/files/validata_responses/<schema>/<file name>.json,
with the hashes of the schema & of the file: if one of them changes, the response is stale (the test fails).

Record the missing or stale responses (calls the live API):
    VALIDATA_RECORD=1 python manage.py test imports

NOTE: Validata reads the schema from GitHub (branch GIT_BRANCH): when a schema changes, push the branch first
(and record with GIT_BRANCH=<branch>). The recording fails if the schema on GitHub differs from the local one.
"""

import hashlib
import json
import os
from pathlib import Path
from unittest import mock

import requests

from common.api import validata

RESPONSES_FOLDER_PATH = Path(__file__).parent / "files" / "validata_responses"
SCHEMAS_FOLDER_PATH = Path(__file__).resolve().parents[2] / "data" / "schemas" / "imports"
RECORD_RETRIES = 3

# keep a reference to the real function (it is patched during the tests)
validate_file_against_schema_live = validata.validate_file_against_schema


def _hash(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _get_response_path(schema_name, file_name):
    return RESPONSES_FOLDER_PATH / Path(schema_name).stem / f"{file_name}.json"


def _check_schema_on_github(schema_url, schema_content):
    """Validata reads the schema from GitHub: it must be the local one"""
    github_schema = requests.get(schema_url, timeout=30).json()
    if github_schema != json.loads(schema_content):
        raise AssertionError(
            f"Validata replay: the schema on GitHub ({schema_url}) differs from the local one. "
            "Push the branch first, and record with GIT_BRANCH=<branch>."
        )


def _record(file, schema_url, schema_content):
    _check_schema_on_github(schema_url, schema_content)
    # Validata unavailable ("Merci de réessayer plus tard"): an exception is raised, retry (never recorded)
    for attempt in range(1, RECORD_RETRIES + 1):
        try:
            response = validate_file_against_schema_live(file, schema_url)
            break
        except Exception:
            if attempt == RECORD_RETRIES:
                raise
    # remove the fields that change at each call (date, duration) or with GIT_BRANCH (schema url)
    response.pop("date", None)
    response.pop("schema", None)
    response.get("report", {}).get("stats", {}).pop("seconds", None)
    return response


def validate_file_against_schema_replay(file, schema_url):
    schema_name = schema_url.split("/")[-1]
    schema_content = (SCHEMAS_FOLDER_PATH / schema_name).read_bytes()
    file.seek(0)
    file_content = file.read()
    file_content = file_content.encode() if isinstance(file_content, str) else file_content
    file_name = Path(getattr(file, "name", "upload.csv")).name
    key = {"schema": schema_name, "schema_sha256": _hash(schema_content), "file_sha256": _hash(file_content)}

    response_path = _get_response_path(schema_name, file_name)
    recorded = json.loads(response_path.read_text()) if response_path.exists() else None
    if recorded and recorded["key"] == key:
        return recorded["response"]

    if not os.getenv("VALIDATA_RECORD"):
        reason = "stale (the schema or the file changed)" if recorded else "missing"
        raise AssertionError(
            f"Validata replay: the response for {file_name} ({schema_name}) is {reason}. "
            "Record it with: VALIDATA_RECORD=1 python manage.py test imports (see imports/tests/validata_replay.py)"
        )

    response = _record(file, schema_url, schema_content)
    response_path.parent.mkdir(parents=True, exist_ok=True)
    response_path.write_text(
        json.dumps({"key": key, "response": response}, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    )
    return response


class ValidataReplayMixin:
    """
    Import tests: replay the recorded Validata responses (see above)
    Usage: class MyImportTest(ValidataReplayMixin, APITestCase)
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        patcher = mock.patch(
            "common.api.validata.validate_file_against_schema", side_effect=validate_file_against_schema_replay
        )
        patcher.start()
        cls.addClassCleanup(patcher.stop)
