import csv
import hashlib
import io
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
    ALLOWED_FILE_FORMAT = ["text/csv", "text/tab-separated-values", "application/vnd.ms-excel"]
    file_format = get_file_content_type(file)
    has_csv_extension = file._name.lower().endswith((".csv", ".tsv"))
    if file_format not in ALLOWED_FILE_FORMAT or not has_csv_extension:
        raise ValidationError(
            f"Ce fichier est au format {file_format}, merci d'exporter votre fichier au format CSV et réessayer."
        )


def get_file_digest(file):
    file_hash = hashlib.md5()
    for row in file:
        file_hash.update(row)
    return file_hash.hexdigest()


def get_csv_file_dialect(file):
    """
    Possible values: 'excel', 'excel-tab', 'unix'
    """
    file.seek(0)
    row_1 = file.readline()
    (decoded_row, _) = decode_bytes(row_1)
    return csv.Sniffer().sniff(decoded_row)


def verify_first_line_is_header(file, file_dialect, expected_header):
    file.seek(0)
    row_1 = file.readline()
    (decoded_row, _) = decode_bytes(row_1)
    csvreader = csv.reader(io.StringIO("".join(decoded_row)), file_dialect)
    header = next(csvreader)
    if header != expected_header:
        raise ValidationError(
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre"
        )
    return header


def verify_first_line_is_header_list(file, file_dialect, expected_header_list):
    file.seek(0)
    row_1 = file.readline()
    (decoded_row, _) = decode_bytes(row_1)
    csvreader = csv.reader(io.StringIO("".join(decoded_row)), file_dialect)
    header = next(csvreader)
    if header not in expected_header_list:
        raise ValidationError(
            "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre"
        )
    return header
