import logging
import time
import uuid
from decimal import ROUND_HALF_DOWN, Decimal, InvalidOperation

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
import json

from api.permissions import IsAuthenticated
from api.serializers import PurchaseSerializer
from common.api import validata
from common.utils import file_import
from common.utils import utils as utils_utils
from data.models import Canteen, ImportFailure, ImportType, Purchase
from data.models.creation_source import CreationSource

from .utils import camelize

logger = logging.getLogger(__name__)

PURCHASE_SCHEMA_FILE_NAME = "achats.json"
PURCHASE_SCHEMA_FILE_PATH = f"data/schemas/imports/{PURCHASE_SCHEMA_FILE_NAME}"
PURCHASE_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{PURCHASE_SCHEMA_FILE_PATH}"


class PurchasesImportView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        self.purchases = []
        self.errors = []
        self.start_time = None
        self.file_digest = None
        self.tmp_id = uuid.uuid4()
        self.file = None
        self.dialect = None
        self.is_duplicate_file = False
        self.duplicate_purchases = []
        self.duplicate_purchase_count = 0
        self.expected_header = file_import.get_expected_header_from_schema(PURCHASE_SCHEMA_FILE_PATH)
        super().__init__(**kwargs)

    def post(self, request):
        self.start_time = time.time()
        logger.info("Purchase bulk import started")
        try:
            # Header from schema
            schema_file = open(PURCHASE_SCHEMA_FILE_PATH)
            json_data = json.load(schema_file)
            expected_header = [field["name"] for field in json_data["fields"]]

            # File validation
            self.file = request.data["file"]
            file_import.validate_file_size(self.file)
            self.file_digest = file_import.get_file_digest(self.file)
            self._check_duplication()

            # Schema validation (Validata)
            schema_name = PURCHASE_SCHEMA_FILE_NAME
            schema_url = PURCHASE_SCHEMA_URL
            validata_response = validata.validate_file_against_schema(self.file, schema_url)

            # Error generating the report
            if "error" in validata_response:
                error = validata_response["error"]["message"]
                self.errors = [
                    {
                        "message": f"Une erreur inconnue s'est produite en lisant votre fichier : « {error} ». Renouveler votre essai, et si l'erreur persiste contactez le support.",
                        "status": 400,
                    }
                ]
                self._log_error(f"Echec lors de la demande de validation du fichier (schema {schema_name} - Validata)")
                return self._get_success_response()

            # Header validation
            header_has_errors = validata.check_if_has_errors_header(validata_response["report"])
            if header_has_errors:
                self.errors = [
                    {
                        "message": "La première ligne du fichier doit contenir les bon noms de colonnes ET dans le bon ordre. Veuillez écrire en minuscule, vérifiez les accents, supprimez les espaces avant ou après les noms, supprimez toutes colonnes qui ne sont pas dans le modèle ci-dessus.",
                        "status": 400,
                    }
                ]
                self._log_error(f"Echec lors de la validation du header (schema {schema_name} - Validata)")
                return self._get_success_response()

            # Rows validation
            self.errors = validata.process_errors(validata_response["report"])
            if len(self.errors):
                self._log_error(f"Echec lors de la validation du fichier (schema {schema_name} - Validata)")
                return self._get_success_response()

            # ma-cantine validation (permissions, last checks...) + import
            with transaction.atomic():
                self._process_file(validata_response["resource_data"])

                # If at least an error has been detected, we raise an error to interrupt the
                # transaction and rollback the insertion of any data
                if self.errors:
                    raise IntegrityError()

                # Update all purchases's import source with file digest
                Purchase.objects.filter(import_source=self.tmp_id).update(import_source=self.file_digest)

            return self._get_success_response()

        except PermissionDenied as e:
            self._log_error(e.detail)
            self.errors = [{"row": 0, "status": status.HTTP_401_UNAUTHORIZED, "message": e.detail}]
        except IntegrityError as e:
            self._log_error(f"L'import du fichier CSV a échoué: {e}")
        except ValidationError as e:
            self._log_error(e.message)
            self.errors = [{"row": 0, "status": status.HTTP_400_BAD_REQUEST, "message": e.message}]
        except Exception as e:
            message = f"Échec lors de la lecture du fichier: {e}"
            self._log_error(message, "exception")
            self.errors = [{"row": 0, "status": status.HTTP_500_INTERNAL_SERVER_ERROR, "message": message}]
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

    def _process_file(self, data):
        chunk = []
        row_count = 0
        for row_number, row in enumerate(data, start=1):
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

        for row_number, row in enumerate(chunk, start=1):
            try:
                siret = utils_utils.normalize_string(row[0])
                self._create_purchase_for_canteen(siret, row)

            except Exception as e:
                for error in self._parse_errors(e, row, siret):
                    errors.append(PurchasesImportView._get_error(e, error["message"], error["code"], row_number))
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

        description = row[1]
        provider = row[2]
        date = row[3]
        price = row[4].strip().replace(",", ".")

        # We try to round the price. If we can't, we will let Django's field validation
        # manage the error - hence the `pass` in the exception handler
        try:
            price = Decimal(price).quantize(Decimal(".01"), rounding=ROUND_HALF_DOWN)
        except InvalidOperation:
            pass

        family = row[5]
        characteristics = [c.strip() for c in row[6].split(",")] if row[6] else []
        local_definition = row[7].strip() if row[7] else None

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
            creation_source=CreationSource.IMPORT,
        )
        purchase.full_clean()
        self.purchases.append(purchase)

    @staticmethod
    def _get_error(e, message, error_status, row_number):
        return {"row": row_number, "status": error_status, "message": message}

    @staticmethod
    def _get_verbose_field_name(field_name):
        try:
            return Purchase._meta.get_field(field_name).verbose_name
        except Exception:
            return field_name

    def _get_success_response(self):
        return JsonResponse(
            {
                "count": 0 if self.errors else len(self.purchases),
                "errors": self.errors,
                "seconds": time.time() - self.start_time,
                "duplicatePurchases": camelize(PurchaseSerializer(self.duplicate_purchases, many=True).data),
                "duplicateFile": self.is_duplicate_file,
                "duplicatePurchaseCount": self.duplicate_purchase_count,
            },
            status=status.HTTP_200_OK,
        )

    staticmethod

    def _add_error(errors, message, code=400):
        errors.append({"message": message, "code": code})

    def _parse_errors(self, e, row, siret):
        errors = []
        if isinstance(e, PermissionDenied):
            PurchasesImportView._add_error(errors, e.detail, 401)
        elif isinstance(e, ObjectDoesNotExist):
            errors.append(
                {
                    "message": f"Une cantine avec le siret « {siret} » n'existe pas sur la plateforme.",
                    "code": 404,
                }
            )
        elif isinstance(e, ValidationError):
            if hasattr(e, "message_dict"):
                for field, messages in e.message_dict.items():
                    for message in messages:
                        user_message = message
                        PurchasesImportView._add_error(errors, user_message)
        if not errors:
            PurchasesImportView._add_error(errors, "Une erreur s'est produite en créant un achat pour cette ligne")
        return errors
