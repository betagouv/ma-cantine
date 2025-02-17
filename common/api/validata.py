import requests

VALIDATA_PREPROD_API_URL = "https://preprod-api-validata.dataeng.etalab.studio/validate"
VALIDATA_PROD_API_URL = "https://api.validata.etalab.studio/validate"


def validate_file_against_schema(file, schema_url):
    # Reset the file pointer to the beginning
    file.seek(0)
    response = requests.post(
        VALIDATA_PROD_API_URL,
        files={
            "file": ("file.csv", file.read(), file.content_type),
        },
        data={"schema": schema_url, "header_case": True},
    )
    return response.json()["report"]


def process_errors(report):
    errors = []
    for error in report["errors"]:
        errors.append(
            {
                "row": error["rowNumber"],
                "column": error["fieldNumber"],
                "field": error["fieldName"],
                "cell": error["cell"],
                # tags: a list, e.g. ['#table', '#row', '#cell']
                "tags": error["tags"],
                # title: Cellule manquante, Valeur manquante, Format incorrect, Format de date incorrect...
                "title": error["title"],
                "message": error["message"],
                # type: missing-cell, constraint-error, type-error...
                "type": error["type"],
                "status": 400,
            }
        )
    return errors
