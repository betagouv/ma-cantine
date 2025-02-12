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
                # cells, description, fieldNumber, name, note, rowNumber, tags, type
                "row": error["rowPosition"],
                "column": error["fieldPosition"],
                "field": error["fieldName"],
                "cell": error["cell"],
                "title": error["title"],  # Cellule vide, Format incorrect, Format de date incorrect
                "message": error["message"],
                "code": error["code"],
                "status": 400,
            }
        )
    return errors
