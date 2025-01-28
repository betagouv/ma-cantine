import hashlib

from django.conf import settings
from django.core.exceptions import ValidationError


def get_file_size(file):
    return file.size


def validate_file_size(file):
    if get_file_size(file) > settings.CSV_IMPORT_MAX_SIZE:
        raise ValidationError(
            f"Ce fichier est trop grand, merci d'utiliser un fichier de moins de {settings.CSV_IMPORT_MAX_SIZE_PRETTY}"
        )


def get_file_content_type(file):
    return file.content_type


def validate_file_format(file):
    file_format = get_file_content_type(file)
    if file_format not in ["text/csv", "text/tab-separated-values"]:
        raise ValidationError(
            f"Ce fichier est au format {file_format}, merci d'exporter votre fichier au format CSV et réessayer."
        )


def get_file_digest(file):
    file_hash = hashlib.md5()
    for row in file:
        file_hash.update(row)
    return file_hash.hexdigest()
