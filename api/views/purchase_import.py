import uuid
from decimal import ROUND_HALF_DOWN, Decimal, InvalidOperation

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status
from rest_framework.exceptions import PermissionDenied

from api.serializers import PurchaseSerializer
from api.views.base_import import BaseImportView
from common.utils import file_import
from common.utils import utils as utils_utils
from data.models import Canteen, ImportType, Purchase
from data.models.creation_source import CreationSource

from .utils import camelize


PURCHASE_SIRET_SCHEMA_FILE_NAME = "achats_siret.json"
PURCHASE_SIRET_SCHEMA_FILE_PATH = f"data/schemas/imports/{PURCHASE_SIRET_SCHEMA_FILE_NAME}"
PURCHASE_SIRET_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{PURCHASE_SIRET_SCHEMA_FILE_PATH}"
PURCHASE_ID_SCHEMA_FILE_NAME = "achats_id.json"
PURCHASE_ID_SCHEMA_FILE_PATH = f"data/schemas/imports/{PURCHASE_ID_SCHEMA_FILE_NAME}"
PURCHASE_ID_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{PURCHASE_ID_SCHEMA_FILE_PATH}"
PURCHASE_SIRET_2026_SCHEMA_FILE_NAME = "achats_siret_2026.json"
PURCHASE_SIRET_2026_SCHEMA_FILE_PATH = f"data/schemas/imports/{PURCHASE_SIRET_2026_SCHEMA_FILE_NAME}"
PURCHASE_SIRET_2026_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{PURCHASE_SIRET_2026_SCHEMA_FILE_PATH}"
PURCHASE_ID_2026_SCHEMA_FILE_NAME = "achats_id_2026.json"
PURCHASE_ID_2026_SCHEMA_FILE_PATH = f"data/schemas/imports/{PURCHASE_ID_2026_SCHEMA_FILE_NAME}"
PURCHASE_ID_2026_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{PURCHASE_ID_2026_SCHEMA_FILE_PATH}"

# Accepted values for the optional `schema` parameter on the import endpoint.
# When omitted (or set to SCHEMA_VERSION_DEFAULT), the historical schemas
# (achats_siret.json / achats_id.json) are used. When set to SCHEMA_VERSION_2026,
# the new achats_siret_2026.json / achats_id_2026.json schemas are used instead.
SCHEMA_VERSION_DEFAULT = "default"
SCHEMA_VERSION_2026 = "2026"


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

    def post(self, request):
        # Set import type based on request
        self.is_siret_import = request.data.get("type") == "siret"
        self.is_2026_import = request.data.get("schema") == SCHEMA_VERSION_2026
        self.import_type = ImportType.PURCHASE if self.is_siret_import else ImportType.PURCHASE_ID
        # Override to add file digest check before base processing
        self.file = request.data.get("file")
        if self.file:
            # Validate file size before expensive operations
            if not self._validate_file_size():
                return self._get_success_response()

            # Compute file digest and check for duplication
            if not self._check_file_digest_and_duplication():
                return self._get_success_response()

        return super().post(request)

    def _get_schema_config(self):
        if self.is_2026_import:
            if self.is_siret_import:
                return {
                    "name": PURCHASE_SIRET_2026_SCHEMA_FILE_NAME,
                    "url": PURCHASE_SIRET_2026_SCHEMA_URL,
                    "path": PURCHASE_SIRET_2026_SCHEMA_FILE_PATH,
                }
            return {
                "name": PURCHASE_ID_2026_SCHEMA_FILE_NAME,
                "url": PURCHASE_ID_2026_SCHEMA_URL,
                "path": PURCHASE_ID_2026_SCHEMA_FILE_PATH,
            }
        return {
            "name": PURCHASE_SIRET_SCHEMA_FILE_NAME if self.is_siret_import else PURCHASE_ID_SCHEMA_FILE_NAME,
            "url": PURCHASE_SIRET_SCHEMA_URL if self.is_siret_import else PURCHASE_ID_SCHEMA_URL,
            "path": PURCHASE_SIRET_SCHEMA_FILE_PATH if self.is_siret_import else PURCHASE_ID_SCHEMA_FILE_PATH,
        }

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

    def _check_file_digest_and_duplication(self):
        """
        Compute file digest and check for duplicate imports.

        Returns:
            bool: True if no duplication found, False if file is duplicate
        """
        self.file_digest = file_import.get_file_digest(self.file)
        try:
            self._check_duplication()
            return True
        except ValidationError as e:
            # Duplication check failed, add error and return with duplicate info
            self._log_error(e.message)
            self.errors = [{"row": 0, "status": status.HTTP_400_BAD_REQUEST, "message": e.message}]
            return False

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
        pass

    def _create_purchase_for_canteen(self, identifier, row):
        """Create a purchase object for a canteen from row data"""
        canteen_exists = (
            Canteen.objects.filter(siret=identifier).exists()
            if self.is_siret_import
            else Canteen.objects.filter(id=identifier).exists()
        )
        if not canteen_exists:
            raise ObjectDoesNotExist()
        canteen = Canteen.objects.get(siret=identifier) if self.is_siret_import else Canteen.objects.get(id=identifier)
        if self.request.user not in canteen.managers.all():
            raise PermissionDenied(detail="Vous n'êtes pas un gestionnaire de cette cantine.")

        description = row[1]
        fournisseur = row[2]
        date = row[3]
        prix_ht = row[4]

        # We try to round the price. If we can't, we will let Django's field validation
        # manage the error - hence the `pass` in the exception handler
        try:
            prix_ht = Decimal(prix_ht).quantize(Decimal(".01"), rounding=ROUND_HALF_DOWN)
        except InvalidOperation:
            pass

        famille_produits = row[5]
        caracteristiques = (
            self.get_purchase_caracteristics_2026(row)
            if self.is_2026_import
            else self.get_purchase_caracteristics_before_2026(row)
        )
        definition_local = (
            self.get_purchase_definition_local_2026(row)
            if self.is_2026_import
            else self.get_purchase_definition_local_before_2026(row)
        )

        purchase = Purchase(
            canteen=canteen,
            description=description.strip(),
            fournisseur=fournisseur.strip(),
            date=date.strip(),
            prix_ht=prix_ht,
            famille_produits=famille_produits.strip(),
            caracteristiques=caracteristiques,
            definition_local=definition_local,
            import_source=self.tmp_id,
            creation_user=self.request.user,
            creation_source=CreationSource.IMPORT,
        )
        purchase.full_clean()
        return purchase

    def get_purchase_caracteristics_before_2026(self, row):
        """Get purchase characteristics for before 2026 import schema"""
        return [c.strip() for c in row[6].split(",")] if row[6] else []

    def get_purchase_definition_local_before_2026(self, row):
        """Get local definition for before 2026 import schema"""
        return row[7].strip() if row[7] else None

    def get_purchase_caracteristics_2026(self, row):
        """Get purchase characteristics for 2026 import schema"""
        boolean_true_values = ["oui", "x"]
        # Clean none value
        categories_egalim = row[6].strip() if row[6] else ""
        origine = row[7].strip() if row[7] else ""
        est_local = row[8].strip().lower() if row[8] else ""
        est_circuit_court = row[9].strip().lower() if row[9] else ""
        # Format values for caracteristics
        egalim_caracteristics = categories_egalim.split(",") if categories_egalim else []
        origine_caracteristics = origine.split(",") if origine else []
        local_caracteristics = [Purchase.Characteristic.LOCAL] if est_local in boolean_true_values else []
        circuit_court_caracteristics = (
            [Purchase.Characteristic.CIRCUIT_COURT] if est_circuit_court in boolean_true_values else []
        )
        # Merge caracteristics
        caracteristics = (
            egalim_caracteristics + origine_caracteristics + local_caracteristics + circuit_court_caracteristics
        )
        return caracteristics

    def get_purchase_definition_local_2026(self, row):
        """Get local definition for 2026 import schema"""
        est_local = row[8].strip() if row[8] else ""
        definition_local = row[10].strip() if row[10] else ""
        return definition_local if est_local == "x" else ""

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

    def _get_not_found_message(self, identifier):
        """Get error message for object not found"""
        identifier_name = "le siret" if self.is_siret_import else "l'id"
        return f"Une cantine avec {identifier_name} « {identifier} » n'existe pas sur la plateforme."
