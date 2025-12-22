"""
https://validata.fr

Response keys:
- schema
- url (None in our case)
- options
- version
- date
- report (optional: only if there is no errors in the request)
- error (optional: only if an error occurred during the request or the schema)
- resource_data (optional: only if "include_resource_data" is True in the request)

Possible error keys:
- cell
- fieldName
- fieldNumber
- message
- rowNumber
- tags: a list. e.g. ['#table', '#row', '#cell']
- title: e.g. 'Cellule manquante', 'Valeur manquante', 'Format incorrect', 'Format de date incorrect'...
- type: e.g. 'missing-cell', 'constraint-error', 'type-error', 'blank-row'...
"""

import requests

VALIDATA_PREPROD_API_URL = "https://preprod-api-validata.dataeng.etalab.studio/validate"
VALIDATA_PROD_API_URL = "https://api.validata.etalab.studio/validate"


def validate_file_against_schema(file, schema_url):
    try:
        # Reset the file pointer to the beginning
        file.seek(0)
        response = requests.post(
            VALIDATA_PROD_API_URL,
            files={
                "file": (file.name, file.read(), file.content_type),
            },
            data={"schema": schema_url, "ignore_header_case": True, "include_resource_data": True},
        )
        return response.json()
    except Exception:
        raise Exception("Erreur lors de la validation du fichier (Validata). Merci de réessayer plus tard.")


def process_errors(report):
    errors = []
    for error in report["errors"]:
        common_informations = get_common_error_informations(error)
        specific_informations = get_specific_error_informations(error)
        error_informations = common_informations | specific_informations
        errors.append(error_informations)
    return errors


def check_if_has_errors_header(report):
    # Example "blank-label"
    if any("rowNumber" not in error for error in report["errors"]):
        return True
    # Examples "Colonne manquante", "Colonne surnuméraire"
    if any("Colonne" in warning for warning in report["warnings"]):
        return True
    return False


def get_common_error_informations(error):
    return {
        "row": error["rowNumber"],
        "tags": error["tags"],
        "message": error["message"],
        "type": error["type"],
        "status": 400,
    }


def get_specific_error_informations(error):
    if error["type"] == "blank-row":
        return {
            "title": "Valeur incorrect",
            # "column": "",
            "field": "ligne vide",
            # "cell": "",
            "has_doc": False,
        }
    return {
        "title": error["title"],
        "column": error["fieldNumber"],
        "field": error["fieldName"],
        "cell": error["cell"],
        "has_doc": True,
    }
