import requests

VALIDATA_PREPROD_API_URL = "https://preprod-api-validata.dataeng.etalab.studio/validate"
VALIDATA_PROD_API_URL = "https://api.validata.etalab.studio/validate"


def validate_file_against_schema(file, schema_url):
    # Reset the file pointer to the beginning
    file.seek(0)
    response = requests.post(
        VALIDATA_PREPROD_API_URL,
        files={
            "file": ("file.csv", file.read(), file.content_type),
        },
        data={"schema": schema_url, "header_case": True},
    )
    return response.json()["report"]


def process_errors(report):
    errors = []
    for error in report["errors"]:
        common_informations = get_common_error_informations(error)
        specific_informations = get_specific_error_informations(error)
        error_informations = common_informations | specific_informations
        errors.append(error_informations)
    return errors


def get_common_error_informations(error):
    return {
        "row": error["rowNumber"],
        # tags: a list, e.g. ['#table', '#row', '#cell']
        "tags": error["tags"],
        "message": error["message"],
        # type: missing-cell, constraint-error, type-error...
        "type": error["type"],
        "status": 400,
    }


def get_specific_error_informations(error):
    if error["type"] == "blank-row":
        return {
            "field": "lignes vides",
            "cell": "",
            "title": "Valeur incorrect",
            "has_doc": False,
        }
    else:
        return {
            # title: Cellule manquante, Valeur manquante, Format incorrect, Format de date incorrect...
            "title": error["title"],
            # "column": error["fieldNumber"]
            "field": error["fieldName"],
            "cell": error["cell"],
            "has_doc": True,
        }
