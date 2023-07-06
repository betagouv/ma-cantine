import csv
import time
import logging
from django.db import IntegrityError, transaction
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import BadRequest, ObjectDoesNotExist, ValidationError
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from api.permissions import IsAuthenticated
from data.models import Purchase, Canteen
from .utils import normalise_siret

logger = logging.getLogger(__name__)


class ImportPurchasesView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        self.purchases_created = 0
        super().__init__(**kwargs)

    def post(self, request):
        start = time.time()
        logger.info("Purchase bulk import started")
        try:
            with transaction.atomic():
                file = request.data["file"]
                ImportPurchasesView._verify_file_size(file)
                (purchases, errors) = self._treat_csv_file(file)

                if errors:
                    raise IntegrityError()

            return ImportPurchasesView._get_success_response([], self.purchases_created, errors, start)

        except IntegrityError as e:
            logger.warning(f"L'import du fichier CSV a échoué:\n{e}")
            return ImportPurchasesView._get_success_response([], 0, errors, start)

        except UnicodeDecodeError as e:
            message = e.reason
            logger.warning(f"UnicodeDecodeError: {message}")
            self.errors = [{"row": 0, "status": 400, "message": "Le fichier doit être sauvegardé en Unicode (utf-8)"}]
            return ImportPurchasesView._get_success_response([], 0, errors, start)

        except ValidationError as e:
            message = e.message
            logger.warning(message)
            message = message
            errors = [{"row": 0, "status": 400, "message": message}]
            return ImportPurchasesView._get_success_response([], 0, errors, start)

        except Exception as e:
            message = "Échec lors de la lecture du fichier"
            logger.exception(f"{message}:\n{e}")
            errors = [{"row": 0, "status": 400, "message": message}]
            return ImportPurchasesView._get_success_response([], 0, errors, start)

    @staticmethod
    def _verify_file_size(file):
        if file.size > settings.CSV_IMPORT_MAX_SIZE:
            raise ValidationError("Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo")

    def _treat_csv_file(self, file):
        purchases = []
        errors = []

        filestring = file.read().decode("utf-8-sig")
        filelines = filestring.splitlines()

        if len(filelines) > settings.CSV_PURCHASES_MAX_LINES:
            return (
                [],
                [
                    ImportPurchasesView._get_error(
                        "Too many lines",
                        f"Le fichier ne peut pas contenir plus de {settings.CSV_PURCHASES_MAX_LINES} lignes.",
                        400,
                        len(filelines),
                    )
                ],
            )

        dialect = csv.Sniffer().sniff(filelines[0])

        csvreader = csv.reader(filelines, dialect=dialect)
        import_source = f"Import du fichier CSV {timezone.now()}"
        for row_number, row in enumerate(csvreader, start=1):
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
                purchase = self._create_purchase_for_canteen(siret, row, import_source)
                purchases.append(purchase)

            except Exception as e:
                for error in self._parse_errors(e, row):
                    errors.append(ImportPurchasesView._get_error(e, error["message"], error["code"], row_number))
        return (purchases, errors)

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
        purchase.save()
        self.purchases_created += 1

        return purchase

    @staticmethod
    def _get_success_response(purchases, count, errors, start_time):
        return JsonResponse(
            {
                "purchases": purchases,
                "count": count,
                "errors": errors,
                "seconds": time.time() - start_time,
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
