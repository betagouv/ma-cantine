import csv
import hashlib
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
from data.models import Canteen, ImportFailure, ImportType, Purchase

from .utils import camelize, decode_bytes, normalise_siret

logger = logging.getLogger(__name__)


class ImportPurchasesView(APIView):
    permission_classes = [IsAuthenticated]
    max_error_items = 30

    def __init__(self, **kwargs):
        self.purchases = []
        self.errors = []
        self.start = None
        self.file_digest = None
        self.tmp_id = uuid.uuid4()
        self.file = None
        self.dialect = None
        self.encoding_detected = None
        self.is_duplicate_file = False
        self.duplicate_purchases = []
        self.duplicate_purchase_count = 0
        super().__init__(**kwargs)

    def post(self, request):
        self.start = time.time()
        logger.info("Purchase bulk import started")
        try:
            self.file = request.data["file"]
            self._verify_file_size()
            with transaction.atomic():
                self._process_file()

                # If at least an error has been detected, we raise an error to interrupt the
                # transaction and rollback the insertion of any data
                if self.errors:
                    raise IntegrityError()

                # The duplication check is called after the processing. The cost of eventually processing
                # the file for nothing appears to be smaller than read the file twice.
                self._check_duplication()

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
        file_hash = hashlib.md5()
        chunk = []
        row_count = 1
        for row in self.file:
            # Sniffing header
            if self.dialect is None:
                # decode header, discarding encoding result that might not be accurate without more data
                (decoded_row, _) = decode_bytes(row)
                self.dialect = csv.Sniffer().sniff(decoded_row)

            file_hash.update(row)

            # Split into chunks
            chunk.append(row)

            # Process full chunk
            if row_count == settings.CSV_PURCHASE_CHUNK_LINES:
                self._process_chunk(chunk)
                chunk = []
                row_count = 0
            row_count += 1

        # Process the last chunk
        if len(chunk) > 0:
            self._process_chunk(chunk)

        self.file_digest = file_hash.hexdigest()

    def _verify_file_size(self):
        if self.file.size > settings.CSV_IMPORT_MAX_SIZE:
            raise ValidationError("Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo")

    def _decode_chunk(self, chunk_list):
        if self.encoding_detected is None:
            chunk = b"".join(chunk_list)
            (_, encoding) = decode_bytes(chunk)
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
            # If header, pass
            if row_number == 1 and row[0].lower().__contains__("siret"):
                continue
            try:
                # first check that the number of columns is good
                #   to throw error if badly formatted early on.
                if len(row) < 7:
                    raise BadRequest()
                siret = row.pop(0)
                if siret == "":
                    raise ValidationError({"siret": "Le siret de la cantine ne peut pas être vide"})
                siret = normalise_siret(siret)
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
        if description == "":
            raise ValidationError({"description": "La description ne peut pas être vide"})
        provider = row.pop(0)
        if provider == "":
            raise ValidationError({"provider": "Le fournisseur ne peut pas être vide"})
        date = row.pop(0)
        if date == "":
            raise ValidationError({"date": "La date ne peut pas être vide"})

        price = row.pop(0).strip().replace(",", ".")
        if price == "":
            raise ValidationError({"price_ht": "Le prix ne peut pas être vide"})

        # We try to round the price. If we can't, we will let Django's field validation
        # manage the error - hence the `pass` in the exception handler
        try:
            price = Decimal(price).quantize(Decimal(".01"), rounding=ROUND_HALF_DOWN)
        except InvalidOperation:
            pass

        family = row.pop(0)
        characteristics = row.pop(0)
        characteristics = [c.strip() for c in characteristics.split(",")]
        local_definition = ImportPurchasesView._get_local_definition(row, characteristics)

        purchase = Purchase(
            canteen=canteen,
            description=description.strip(),
            provider=provider.strip(),
            date=date.strip(),
            price_ht=price,
            family=family.strip(),
            characteristics=characteristics,
            local_definition=local_definition,
            import_source=self.tmp_id,
        )
        purchase.full_clean()
        self.purchases.append(purchase)

    # Factored out because _create_purchase_for_canteen was too complex for flake8 validation
    @staticmethod
    def _get_local_definition(row, characteristics):
        local_definition = None
        if "LOCAL" in characteristics:
            try:
                local_definition = row.pop(0)
                if not local_definition:
                    raise IndexError
            except IndexError:
                raise ValidationError(
                    {"local_definition": "La définition de local est obligatoire pour les produits locaux"}
                )
        return local_definition.strip() if local_definition else None

    def _get_success_response(self):
        return JsonResponse(
            {
                "count": 0 if self.errors else len(self.purchases),
                "errorCount": len(self.errors),
                "errors": self.errors[: self.max_error_items],
                "seconds": time.time() - self.start,
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
                    "message": f"Format fichier : 7-8 colonnes attendues, {len(row)} trouvées.",
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
                    verbose_field_name = ImportPurchasesView._get_verbose_field_name(field)
                    for message in messages:
                        user_message = message
                        if field != "__all__":
                            user_message = f"Champ '{verbose_field_name}' : {user_message}"
                        errors.append(
                            {
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
