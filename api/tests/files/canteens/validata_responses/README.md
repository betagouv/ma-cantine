# Validata test fixtures

These JSON files are real responses captured from the live [Validata API](https://validata.fr),
one per CSV/XLSX file in `api/tests/files/canteens/` that's used by
`api/tests/test_canteens_create_import.py` and `api/tests/test_canteens_update_import.py`.

They exist so those tests don't depend on a live network call to a third-party service during
CI (see `mock_validata_response()` in `api/tests/utils.py`), which was a source of flaky test
failures.

## When to regenerate

- You changed the **content** of one of the CSV/XLSX fixture files in `api/tests/files/canteens/`
  (the captured response includes both the parsed row data and the validation errors, so it goes
  stale if the source file changes).
- You added a **new** `mock_validata_response(mock, "some_file.csv")` call for a file that doesn't
  have a fixture yet.
- The **import schema** changed (`data/schemas/imports/cantines_creer.json` or
  `cantines_modifier.json`), which can change which errors Validata reports.

If a test that uses one of these fixtures starts failing after any of the above, regenerating is
the first thing to try.

## How to regenerate

Requires internet access (it calls the real Validata API):

```bash
# Regenerate everything referenced by the create/update import tests
python manage.py generate_validata_test_fixtures

# Regenerate just specific files
python manage.py generate_validata_test_fixtures canteens_good.csv canteens_bad.csv
```

Then review the diff and commit the updated `.json` file(s) alongside your change.
