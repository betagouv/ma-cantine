# Validata test fixtures

Each `<category>/validata_responses/*.json` file (e.g. `canteens/validata_responses/`,
`achats/validata_responses/`) is a real response captured from the live
[Validata API](https://validata.fr), one per CSV/XLSX fixture file used by an import test.

They exist so import tests don't depend on a live network call to a third-party service during
CI (see `mock_validata_response()` in `api/tests/utils.py`), which was a source of flaky test
failures. Covered import test files: `test_canteens_create_import.py`,
`test_canteens_update_import.py`, `test_canteens_managers_import.py`, `test_purchases_import.py`,
`test_purchases_import_old.py`, `test_diagnostics_complete_import.py`,
`test_diagnostics_simple_import.py`.

## When to regenerate

- You changed the **content** of one of the CSV/XLSX fixture files (the captured response
  includes both the parsed row data and the validation errors, so it goes stale if the source
  file changes).
- You added a **new** `mock_validata_response(mock, "some_file.csv", category="...")` call for a
  file that doesn't have a fixture yet.
- The **import schema** changed (`data/schemas/imports/*.json`), which can change which errors
  Validata reports.

If a test that uses one of these fixtures starts failing after any of the above, regenerating is
the first thing to try.

## How to regenerate

Requires internet access (it calls the real Validata API):

```bash
# Regenerate every fixture referenced across all import tests
python manage.py generate_validata_test_fixtures

# Regenerate just specific files (matched by filename, regardless of category)
python manage.py generate_validata_test_fixtures canteens_good.csv purchases_good.csv
```

Then review the diff and commit the updated `.json` file(s) alongside your change. Regenerating
without any real content/schema change should produce an empty diff (the command strips the
response's timestamp and processing-duration fields, which otherwise change on every call).

## Adding a new import type / schema variant

The command discovers which fixtures exist by scanning each covered test file for
`mock_validata_response(mock, "<filename>", category="<category>")` calls — there's no separate
list to keep in sync. `category` doubles as both the `api/tests/files/<category>/` subdirectory
the source file lives in, and the schema/fixture namespace, so most import types just need one
call site each. If a single test file validates against more than one schema (e.g.
diagnostics-simple import by SIRET vs by id, or achats import by SIRET vs by id), pass a distinct
`category` per schema at each call site — see `SCHEMA_URLS` and `SOURCE_DIR_OVERRIDES` in
`macantine/management/commands/generate_validata_test_fixtures.py` for how those map to schema
URLs.
