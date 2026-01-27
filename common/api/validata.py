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


def process_header_errors(user_file_header, expected_header):
    header_errors = []
    diff_header_length = len(user_file_header) - len(expected_header)

    # Missing columns
    if diff_header_length < 0:
        header_errors.append(
            {
                "field": "Première ligne du fichier incorrecte",
                # "column": "",
                # "cell": "",
                "has_doc": False,
                "title": "Elle doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
            }
        )
        # Stop here because the header is invalid
        return header_errors

    # Extra columns
    if diff_header_length > 0:
        field = (
            f"{diff_header_length} colonnes supplémentaires" if diff_header_length > 1 else "1 colonne supplémentaire"
        )
        title = (
            f"Supprimer les {diff_header_length} colonnes en excès et toutes les données présentes dans ces dernières."
            if diff_header_length > 1
            else "Supprimer la colonne en excès et toutes les données présentes dans cette dernière."
        )
        title += " Il se peut qu'un espace ou un symbole invisible soit présent dans votre fichier, en cas de doute faite un copier-coller des données dans un nouveau document."
        header_errors.append(
            {
                "field": field,
                # "column": "",
                # "cell": "",
                "has_doc": False,
                "title": title,
            }
        )

    # Incorrect column names
    for index, expected_column_name in enumerate(expected_header):
        if index >= len(user_file_header):
            break
        if expected_column_name != user_file_header[index]:
            header_errors.append(
                {
                    "field": f"colonne {expected_column_name}",
                    # "column": index,
                    # "cell": 0,
                    "has_doc": False,
                    "title": f"Valeur incorrecte vous avez écrit « {user_file_header[index]} » au lieu de « {expected_column_name} »",
                }
            )

    return header_errors


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
            "title": "Valeur incorrecte la ligne doit être supprimée",
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
