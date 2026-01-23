import uuid
from decimal import ROUND_HALF_DOWN, Decimal, InvalidOperation

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework.exceptions import PermissionDenied

from api.serializers import PurchaseSerializer
from api.views.base_import import BaseImportView
from common.api import validata
from common.utils import file_import
from common.utils import utils as utils_utils
from data.models import Canteen, ImportType, Purchase
from data.models.creation_source import CreationSource

from .utils import camelize


PURCHASE_SCHEMA_FILE_NAME = "achats.json"
PURCHASE_SCHEMA_FILE_PATH = f"data/schemas/imports/{PURCHASE_SCHEMA_FILE_NAME}"
PURCHASE_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{PURCHASE_SCHEMA_FILE_PATH}"


class PurchasesImportView(BaseImportView):
    import_type = ImportType.PURCHASE
    model_class = Purchase

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.purchases = []
        self.file_digest = None
        self.tmp_id = uuid.uuid4()
        self.is_duplicate_file = False
        self.duplicate_purchases = []
        self.duplicate_purchase_count = 0
        self.expected_header = file_import.get_expected_header_from_schema(PURCHASE_SCHEMA_FILE_PATH)

    def post(self, request):
        # Override to add file digest check before base processing
        self.file = request.data.get("file")
        if self.file:
            file_import.validate_file_size(self.file)
            self.file_digest = file_import.get_file_digest(self.file)
            try:
                self._check_duplication()
            except ValidationError:
                # Duplication check failed, return response with duplicate info
                return self._get_success_response()

        return super().post(request)

    def _get_schema_config(self):
        return {
            "name": PURCHASE_SCHEMA_FILE_NAME,
            "url": PURCHASE_SCHEMA_URL,
        }

    def _validate_header(self, validata_response, schema_name):
        """Custom header validation for purchases"""
        user_file_header = validata_response["resource_data"][0]
        self.errors = validata.process_header_errors(user_file_header, self.expected_header)
        if len(self.errors):
            self._log_error(f"Echec lors de la validation du header (schema {schema_name} - Validata)")
            return False
        return True

    def _process_file(self, data):
        """Process file with chunking for better performance"""
        chunk = []
        row_count = 0
        for row_number, row in enumerate(data, start=1):
            if row_number == 1:  # skip header
                continue
            # Split into chunks
            chunk.append((row_number, row))
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
        """Process a chunk of rows and bulk insert if no errors"""
        errors = []
        chunk_purchases = []

        for row_number, row in chunk:
            try:
                siret = utils_utils.normalize_string(row[0])
                purchase = self._create_purchase_for_canteen(siret, row)
                chunk_purchases.append(purchase)

            except Exception as e:
                identifier = siret if siret else None
                for error in self._parse_errors(e, row, identifier):
                    errors.append(self._get_error(e, error["message"], error["code"], row_number))

        self.errors += errors

        # If no error has been detected in the file so far, we insert the chunk into the db
        if not self.errors:
            Purchase.objects.bulk_create(chunk_purchases)
            self.purchases.extend(chunk_purchases)

    def _save_data_from_row(self, row):
        """Not used in purchase import due to chunking, but required by base class"""
        siret = utils_utils.normalize_string(row[0])
        return self._create_purchase_for_canteen(siret, row)

    def _create_purchase_for_canteen(self, siret, row):
        """Create a purchase object for a canteen from row data"""
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
        return purchase

    def _post_process_file(self):
        """Update all purchases's import source with file digest"""
        if not self.errors:
            Purchase.objects.filter(import_source=self.tmp_id).update(import_source=self.file_digest)

    def _get_response_data(self):
        """Return purchase-specific response data"""
        return {
            "count": len(self.purchases),
            "duplicatePurchases": camelize(PurchaseSerializer(self.duplicate_purchases, many=True).data),
            "duplicateFile": self.is_duplicate_file,
            "duplicatePurchaseCount": self.duplicate_purchase_count,
        }

    def _get_generic_error_message(self):
        return "Une erreur s'est produite en créant un achat pour cette ligne"
