import csv
import hashlib
import logging

import chardet
from django.conf import settings
from django.core.exceptions import ValidationError

logger = logging.getLogger(__name__)


def decode_bytes(bytes_string):
    detection_result = chardet.detect(bytes_string)
    encoding_detected = detection_result["encoding"]
    logger.info(f"Encoding autodetected : {encoding_detected}")
    return (bytes_string.decode(encoding_detected), encoding_detected)


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


def get_csv_file_dialect(file):
    file.seek(0)
    row_1 = file.readline()
    (decoded_row, _) = decode_bytes(row_1)
    return csv.Sniffer().sniff(decoded_row)
