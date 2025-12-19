import csv
import io
import logging
import time
import uuid
from decimal import ROUND_HALF_DOWN, Decimal, InvalidOperation

from django.conf import settings
from django.core.exceptions import BadRequest, ObjectDoesNotExist, ValidationError
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView

from api.permissions import IsAuthenticated
from api.serializers import PurchaseSerializer
from common.api import validata
from common.utils import file_import
from common.utils import utils as utils_utils
from data.models import Canteen, ImportFailure, ImportType, Purchase
from data.models.creation_source import CreationSource

from .utils import camelize

logger = logging.getLogger(__name__)


PURCHASE_SCHEMA_FILE_PATH = "data/schemas/imports/achats.json"
PURCHASE_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{PURCHASE_SCHEMA_FILE_PATH}"


class ImportPurchasesView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        self.purchases = []
        self.errors = []
        self.start_time = None
        self.file_digest = None
        self.tmp_id = uuid.uuid4()
        self.file = None
        self.dialect = None
        self.encoding_detected = None
        self.is_duplicate_file = False
        self.duplicate_purchases = []
        self.duplicate_purchase_count = 0
        self.header = None
        self.schema_url = PURCHASE_SCHEMA_URL
        self.expected_header = file_import.get_expected_header_from_schema(PURCHASE_SCHEMA_FILE_PATH)
        super().__init__(**kwargs)

    def post(self, request):
        self.start_time = time.time()
        logger.info("Purchase bulk import started")
        try:
            self.file = request.data["file"]

            # Step 1: Format validation
            file_import.validate_file_size(self.file)

            self.file_digest = file_import.get_file_digest(self.file)
            self._check_duplication()

            self.dialect = file_import.get_csv_file_dialect(self.file)
            self.header = file_import.verify_first_line_is_header(self.file, self.dialect, self.expected_header)

            # Step 2: Schema validation (Validata)
            validata_response = validata.validate_file_against_schema(self.file, self.schema_url)
            report = validata_response["report"]
            self.errors = validata.process_errors(report)
            if len(self.errors):
                self._log_error("Echec lors de la validation du fichier (schema achats.json - Validata)")
                return self._get_success_response()

            # Step 3: ma-cantine validation (permissions, last checks...) + import
            with transaction.atomic():
                self._process_file()

                # If at least an error has been detected, we raise an error to interrupt the
                # transaction and rollback the insertion of any data
                if self.errors:
                    raise IntegrityError()

                # Update all purchases's import source with file digest
                Purchase.objects.filter(import_source=self.tmp_id).update(import_source=self.file_digest)

            return self._get_success_response()

        except IntegrityError as e:
            self._log_error(f"L'import du fichier CSV a échoué:\n{e}")
            return self._get_success_response()

        except UnicodeDecodeError as e:
            self._log_error(f"UnicodeDecodeError: {e.reason}")
            self.errors = [{"row": 0, "status": 400, "message": "Le fichier doit être sauvegardé en Unicode (utf-8)"}]
            return self._get_success_response()

        except ValidationError as e:
            self._log_error(e.message)
            self.errors = [{"row": 0, "status": 400, "message": e.message}]
            return self._get_success_response()

        except Exception as e:
            message = "Échec lors de la lecture du fichier"
            self._log_error(f"{message}:\n{e}", "exception")
            self.errors = [{"row": 0, "status": 400, "message": message}]
            return self._get_success_response()

    def _log_error(self, message, level="warning"):
        logger_function = getattr(logger, level)
        logger_function(message)
        ImportFailure.objects.create(
            user=self.request.user,
            file=self.file,
            details=message,
            import_type=ImportType.PURCHASE,
        )

    def _process_file(self):
        chunk = []
        row_count = 0
        for row_number, row in enumerate(self.file, start=1):
            if row_number == 1:  # skip header
                continue

            # Split into chunks
            chunk.append(row)
            row_count += 1

            # Process full chunk
            if row_count == settings.CSV_PURCHASE_CHUNK_LINES:
                self._process_chunk(chunk)
                chunk = []
                row_count = 0

        # Process the last chunk
        if len(chunk) > 0:
            self._process_chunk(chunk)

    def _decode_chunk(self, chunk_list):
        if self.encoding_detected is None:
            chunk = b"".join(chunk_list)
            (_, encoding) = file_import.decode_bytes(chunk)
            self.encoding_detected = encoding
        return [chunk.decode(self.encoding_detected) for chunk in chunk_list]

    def _check_duplication(self):
        matching_purchases = Purchase.objects.filter(import_source=self.file_digest)
        if matching_purchases.exists():
            self.duplicate_purchases = matching_purchases[:10]
            self.is_duplicate_file = True
            self.duplicate_purchase_count = matching_purchases.count()
            raise ValidationError("Ce fichier a déjà été utilisé pour un import")

    def _process_chunk(self, chunk):
        errors = []
        self.purchases = []

        decoded_chunk = self._decode_chunk(chunk)
        csvreader = csv.reader(io.StringIO("".join(decoded_chunk)), self.dialect)
        for row_number, row in enumerate(csvreader, start=1):
            siret = None

            try:
                # first check that the number of columns is good
                #   to throw error if badly formatted early on.
                if len(row) < len(self.expected_header):
                    raise BadRequest()
                siret = row.pop(0)
                if siret == "":
                    raise ValidationError({"siret": "Le siret de la cantine ne peut pas être vide"})
                siret = utils_utils.normalize_string(siret)
                self._create_purchase_for_canteen(siret, row)

            except Exception as e:
                for error in self._parse_errors(e, row, siret):
                    errors.append(ImportPurchasesView._get_error(e, error["message"], error["code"], row_number))
        self.errors += errors

        # If no error has been detected in the file so far, we insert the chunk into the db
        if not self.errors:
            Purchase.objects.bulk_create(self.purchases)

    def _create_purchase_for_canteen(self, siret, row):
        if not Canteen.objects.filter(siret=siret).exists():
            raise ObjectDoesNotExist()
        canteen = Canteen.objects.get(siret=siret)
        if self.request.user not in canteen.managers.all():
            raise PermissionDenied(detail="Vous n'êtes pas un gestionnaire de cette cantine.")

        description = row.pop(0)
        provider = row.pop(0)
        date = row.pop(0)
        price = row.pop(0).strip().replace(",", ".")

        # We try to round the price. If we can't, we will let Django's field validation
        # manage the error - hence the `pass` in the exception handler
        try:
            price = Decimal(price).quantize(Decimal(".01"), rounding=ROUND_HALF_DOWN)
        except InvalidOperation:
            pass

        family = row.pop(0)
        characteristics = row.pop(0)
        characteristics = [c.strip() for c in characteristics.split(",")]
        local_definition = row.pop(0)

        purchase = Purchase(
            canteen=canteen,
            description=description.strip(),
            provider=provider.strip(),
            date=date.strip(),
            price_ht=price,
            family=family.strip(),
            characteristics=characteristics,
            local_definition=local_definition.strip(),
            import_source=self.tmp_id,
            creation_source=CreationSource.IMPORT,
        )
        purchase.full_clean()
        self.purchases.append(purchase)

    def _get_success_response(self):
        return JsonResponse(
            {
                "count": 0 if self.errors else len(self.purchases),
                "errorCount": len(self.errors),
                "errors": self.errors,
                "seconds": time.time() - self.start_time,
                "duplicatePurchases": camelize(PurchaseSerializer(self.duplicate_purchases, many=True).data),
                "duplicateFile": self.is_duplicate_file,
                "duplicatePurchaseCount": self.duplicate_purchase_count,
                "encoding": self.encoding_detected,
            },
            status=status.HTTP_200_OK,
        )

    @staticmethod
    def _get_verbose_field_name(field_name):
        try:
            return Purchase._meta.get_field(field_name).verbose_name
        except Exception:
            return field_name

    @staticmethod
    def _get_error(e, message, error_status, row_number):
        logger.warning(f"Error on row {row_number}:\n{e}\n{message}")
        return {"row": row_number, "status": error_status, "message": message}

    def _parse_errors(self, e, row, siret):
        errors = []
        if isinstance(e, PermissionDenied):
            errors.append(
                {
                    "message": e.detail,
                    "code": 401,
                }
            )
        elif isinstance(e, BadRequest):
            errors.append(
                {
                    "message": f"Format fichier : {len(self.expected_header)} colonnes attendues, {len(row)} trouvées.",
                    "code": 400,
                }
            )
        elif isinstance(e, ObjectDoesNotExist):
            errors.append(
                {
                    "message": f"Une cantine avec le siret « {siret} » n'existe pas sur la plateforme.",
                    "code": 404,
                }
            )
        elif isinstance(e, ValidationError):
            if e.message_dict:
                for field, messages in e.message_dict.items():
                    for message in messages:
                        user_message = message
                        errors.append(
                            {
                                "field": field,
                                "message": user_message,
                                "code": 400,
                            }
                        )
        if not errors:
            errors.append(
                {
                    "message": "Une erreur s'est produite en créant un achat pour cette ligne",
                    "code": 400,
                }
            )
        return errors
