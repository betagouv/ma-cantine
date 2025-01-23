import requests


def validate_file_against_schema(self):
    # Reset the file pointer to the beginning
    self.file.seek(0)
    response = requests.post(
        "https://api.validata.etalab.studio/validate",
        files={
            "file": ("file.csv", self.file.read(), self.file.content_type),
        },
        data={"schema": self.schema_url, "header_case": True},
    )
    return response.json()["report"]
