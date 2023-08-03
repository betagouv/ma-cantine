import csv
import time
import logging
import hashlib
import io
from django.db import IntegrityError, transaction
from django.conf import settings
from django.core.exceptions import BadRequest, ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from api.permissions import IsAuthenticated
from data.models import Purchase, Canteen
from api.serializers import PurchaseSerializer
from .utils import normalise_siret, camelize

logger = logging.getLogger(__name__)


class ImportPurchasesView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        self.purchases = []
        self.purchases_count = 0
        self.errors = []
        self.start = None
        self.file_digest = None
        self.file = None
        super().__init__(**kwargs)

    def _process_file(self):
        file_hash = hashlib.md5()
        chunk_size = settings.FILE_CHUNK_SIZE
        chunk = []
        batch_i = 1
        for row in self.file:
            # Split into chunks
            file_hash.update(row)
            chunk.append(row.decode())

            # Process full chunk
            if batch_i == chunk_size:
                self._process_chunk(chunk)
                chunk = []
                batch_i = 0
            batch_i += 1
            
        # Process the last chunk
        if batch_i < chunk_size and len(chunk) > 0:
            self._process_chunk(chunk)

        # The duplication check is called after the processing. The cost of eventually processing
        # the file for nothing appears to be smaller than reand the file twice.
        self._check_duplication(file_hash)

    def post(self, request):
        self.start = time.time()
        logger.info("Purchase bulk import started")
        try:
            self.file = request.data["file"]
            self._verify_file_size()
            self._process_file()
            if not self.errors:
                with transaction.atomic():
                    self.purchases = Purchase.objects.bulk_create(self.purchases)
            else:
                self.purchases = []
                raise IntegrityError()

            return self._get_success_response()

        except IntegrityError as e:
            logger.warning(f"L'import du fichier CSV a échoué:\n{e}")
            return self._get_success_response()

        except UnicodeDecodeError as e:
            message = e.reason
            logger.warning(f"UnicodeDecodeError: {message}")
            self.errors = [{"row": 0, "status": 400, "message": "Le fichier doit être sauvegardé en Unicode (utf-8)"}]
            return self._get_success_response()

        except ValidationError as e:
            message = e.message
            logger.warning(message)
            message = message
            self.errors = [{"row": 0, "status": 400, "message": message}]
            return self._get_success_response()

        except Exception as e:
            message = "Échec lors de la lecture du fichier"
            logger.exception(f"{message}:\n{e}")
            self.errors = [{"row": 0, "status": 400, "message": message}]
            return self._get_success_response()

    def _verify_file_size(self):
        if self.file.size > settings.CSV_IMPORT_MAX_SIZE:
            raise ValidationError("Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo")

    def _check_duplication(self, m):
        try:
            self.file_digest = m.hexdigest()
            matching_purchases = Purchase.objects.filter(import_source=self.file_digest)
        except Exception as e:
            print(e)
        if matching_purchases.exists():
            self.purchases = matching_purchases.all()
            raise ValidationError("Ce fichier a déjà été utilisé pour un import")

    def _process_chunk(self, chunk):
        errors = []
        csvreader = csv.reader(io.StringIO(''.join(chunk)), delimiter=',')
        import_source = self.file_digest
        for row_number, row in enumerate(csvreader, start=1):
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
                self._create_purchase_for_canteen(siret, row, import_source)

            except Exception as e:
                for error in self._parse_errors(e, row):
                    errors.append(ImportPurchasesView._get_error(e, error["message"], error["code"], row_number))
        self.errors = errors

    @transaction.atomic
    def _create_purchase_for_canteen(self, siret, row, import_source):
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
        price = row.pop(0)
        if price == "":
            raise ValidationError({"price_ht": "Le prix ne peut pas être vide"})
        family = row.pop(0)
        characteristics = row.pop(0)
        characteristics = [c.strip() for c in characteristics.split(",")]
        local_definition = row.pop(0)
        if "LOCAL" in characteristics and not local_definition:
            raise ValidationError(
                {"local_definition": "La définition de local est obligatoire pour les produits locaux"}
            )

        purchase = Purchase(
            canteen=canteen,
            description=description.strip(),
            provider=provider.strip(),
            date=date.strip(),
            price_ht=price.strip(),
            family=family.strip(),
            characteristics=characteristics,
            local_definition=local_definition.strip(),
            import_source=import_source,
        )
        purchase.full_clean()
        self.purchases.append(purchase)

    def _get_success_response(self):
        return JsonResponse(
            {
                "purchases": camelize(PurchaseSerializer(self.purchases[:10], many=True).data),
                "count": len(self.purchases),
                "errors": self.errors,
                "seconds": time.time() - self.start,
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

    def _parse_errors(self, e, row):
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
                    "message": "Cantine non trouvée.",
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
