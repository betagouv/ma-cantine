import requests


def validate_file_against_schema(file, schema_url):
    # Reset the file pointer to the beginning
    file.seek(0)
    response = requests.post(
        "https://api.validata.etalab.studio/validate",
        files={
            "file": ("file.csv", file.read(), file.content_type),
        },
        data={"schema": schema_url, "header_case": True},
    )
    return response.json()["report"]


def process_errors(report):
    errors = []
    for error in report["tasks"][0]["errors"]:
        errors.append(
            {
                "row": error["rowNumber"],
                "status": 400,
                "message": f"Champ '{error['fieldName']}' : Valeur « {error['cell']} » : {error['message']}",
            }
        )
    return errors
