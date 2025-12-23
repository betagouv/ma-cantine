import logging
import re
import time
from abc import ABC, abstractmethod
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from simple_history.utils import update_change_reason

from api.permissions import IsAuthenticated
from common.utils import file_import
from common.api import validata
from data.models import Canteen, Diagnostic, ImportFailure, ImportType
from data.models.creation_source import CreationSource

logger = logging.getLogger(__name__)


DIAGNOSTICS_SCHEMA_FILE_NAME = "bilans_simple.json"
DIAGNOSTICS_SCHEMA_FILE_PATH = f"data/schemas/imports/{DIAGNOSTICS_SCHEMA_FILE_NAME}"
DIAGNOSTICS_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{DIAGNOSTICS_SCHEMA_FILE_PATH}"


class ImportDiagnosticsView(ABC, APIView):
    permission_classes = [IsAuthenticated]
    value_error_regex = re.compile(r"Field '(.+)' expected .+? got '(.+)'.")

    def __init__(self, **kwargs):
        self.diagnostics_created = 0
        self.errors = []
        self.start_time = None
        self.file = None
        super().__init__(**kwargs)

    @property
    @abstractmethod
    def import_type(): ...

    def post(self, request):
        self.start_time = time.time()
        logger.info("Diagnostic bulk import started")
        try:
            with transaction.atomic():
                self.file = request.data["file"]
                file_import.validate_file_size(self.file)

                schema_name = DIAGNOSTICS_SCHEMA_FILE_NAME
                schema_url = DIAGNOSTICS_SCHEMA_URL

                print(self.file)

                # Schema validation (Validata)
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
                    self._log_error(
                        f"Echec lors de la demande de validation du fichier (schema {schema_name} - Validata)"
                    )
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
                    if self.errors:
                        print("ERRREURS ICI")
                        raise IntegrityError()

        except PermissionDenied as e:
            self._log_error(e.detail)
            self.errors = [{"row": 0, "status": 401, "message": e.detail}]
        except IntegrityError as e:
            self._log_error(f"L'import du fichier CSV a échoué: {e}")
        except ValidationError as e:
            self._log_error(e.message)
            self.errors = [{"row": 0, "status": 400, "message": e.message}]
        except Exception as e:
            message = f"Échec lors de la lecture du fichier: {e}"
            self._log_error(message, "exception")
            self.errors = [{"row": 0, "status": 400, "message": message}]

        return self._get_success_response()

    def _log_error(self, message, level="warning"):
        logger_function = getattr(logger, level)
        logger_function(message)
        ImportFailure.objects.create(
            user=self.request.user,
            file=self.file,
            details=message,
            import_type=self.import_type,
        )

    def _process_file(self, data):
        for row_number, row in enumerate(data, start=1):
            siret = row[0]
            try:
                if row_number == 1:  # skip header
                    continue
                self._save_data_from_row(row)
            except Exception as e:
                print("ERREUR 2", row, siret)
                print(self._parse_errors)
                for error in self._parse_errors(e, row, siret):
                    self.errors.append(
                        ImportDiagnosticsView._get_error(e, error["message"], error["code"], row_number + 1)
                    )

    @transaction.atomic
    def _save_data_from_row(self, row):
        siret = row[0]
        if not Canteen.objects.filter(siret=siret).exists():
            raise ObjectDoesNotExist()
        canteen = Canteen.objects.get(siret=siret)
        if self.request.user not in canteen.managers.all():
            raise PermissionDenied(detail="Vous n'êtes pas un gestionnaire de cette cantine.")
        diagnostic_year, values_dict, diagnostic_type = self._validate_diagnostic(row)
        self._update_or_create_diagnostic(canteen, diagnostic_year, values_dict, diagnostic_type)

    @abstractmethod
    def _validate_diagnostic(self, row): ...

    def _update_or_create_diagnostic(self, canteen, diagnostic_year, values_dict, diagnostic_type):
        diagnostic_exists = Diagnostic.objects.filter(canteen=canteen, year=diagnostic_year).exists()
        diagnostic = (
            Diagnostic.objects.get(canteen=canteen, year=diagnostic_year)
            if diagnostic_exists
            else Diagnostic(canteen_id=canteen.id, year=diagnostic_year, creation_source=CreationSource.IMPORT)
        )
        if diagnostic.is_teledeclared:
            raise ValidationError(
                "Ce n'est pas possible de modifier un diagnostic télédéclaré. Veuillez retirer cette ligne, ou annuler la télédéclaration."
            )
        diagnostic.diagnostic_type = diagnostic_type
        for key, value in values_dict.items():
            print("key", key)
            print("value", value)
            setattr(diagnostic, key, value)
        diagnostic.full_clean()
        diagnostic.save()
        update_change_reason(diagnostic, f"Mass CSV import. {self.__class__.__name__[:100]}")
        self.diagnostics_created += 1

    @staticmethod
    def _get_error(e, message, error_status, row_number):
        return {"row": row_number, "status": error_status, "message": message}

    @staticmethod
    def _get_verbose_field_name(field_name):
        try:
            return Canteen._meta.get_field(field_name).verbose_name
        except Exception:
            try:
                return Diagnostic._meta.get_field(field_name).verbose_name
            except Exception:
                pass
        return field_name

    def _get_success_response(self):
        body = {
            "count": 0 if len(self.errors) else self.diagnostics_created,
            "errors": self.errors,
            "errorCount": len(self.errors),
            "seconds": time.time() - self.start_time,
        }
        return JsonResponse(body, status=status.HTTP_200_OK)

    @staticmethod
    def _add_error(errors, message, code=400):
        errors.append({"message": message, "code": code})

    def _parse_errors(self, e, row, siret):  # noqa: C901
        errors = []
        if isinstance(e, PermissionDenied):
            ImportDiagnosticsView._add_error(errors, e.detail, 401)
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
                    verbose_field_name = ImportDiagnosticsView._get_verbose_field_name(field)
                    for message in messages:
                        user_message = message
                        if field != "__all__":
                            # TODO : delete
                            user_message = f"Champ '{verbose_field_name}' : {user_message}"
                        ImportDiagnosticsView._add_error(errors, user_message)
            elif hasattr(e, "message"):
                ImportDiagnosticsView._add_error(errors, e.message)
            # TODO : delete ?
            elif hasattr(e, "params"):
                ImportDiagnosticsView._add_error(errors, f"La valeur '{e.params['value']}' n'est pas valide.")
            else:
                ImportDiagnosticsView._add_error(
                    errors, "Une erreur s'est produite en créant un bilan pour cette ligne"
                )
        # TODO : delete ?
        elif isinstance(e, ValueError):
            match = self.value_error_regex.search(str(e))
            field_name = match.group(1) if match else ""
            value_given = match.group(2) if match else ""
            if field_name:
                verbose_field_name = ImportDiagnosticsView._get_verbose_field_name(field_name)
                ImportDiagnosticsView._add_error(
                    errors, f"La valeur '{value_given}' n'est pas valide pour le champ '{verbose_field_name}'."
                )
        if not errors:
            ImportDiagnosticsView._add_error(errors, "Une erreur s'est produite en créant un bilan pour cette ligne")
        return errors


class DiagnosticsSimpleImportView(ImportDiagnosticsView):
    import_type = ImportType.DIAGNOSTIC_SIMPLE

    def _validate_diagnostic(self, row):
        values_dict = {}
        value_fields = [
            "valeur_totale",
            "valeur_bio",
            "valeur_bio_dont_commerce_equitable",
            "valeur_siqo",
            "valeur_externalites_performance",
            "valeur_egalim_autres",
            "valeur_egalim_autres_dont_commerce_equitable",
            "valeur_viandes_volailles",
            "valeur_viandes_volailles_egalim",
            "valeur_viandes_volailles_france",
            "valeur_produits_de_la_mer",
            "valeur_produits_de_la_mer_egalim",
            "valeur_produits_de_la_mer_france",
            "valeur_fruits_et_legumes_france",
            "valeur_charcuterie_france",
            "valeur_produits_laitiers_france",
            "valeur_boulangerie_france",
            "valeur_boissons_france",
            "valeur_autres_france",
        ]
        diagnostic_year = row[1]
        offset_row = 2  # Two columns before value_fields in row
        for idx, value in enumerate(value_fields):
            value_idx = idx + offset_row
            values_dict[value] = None if not row[value_idx] else Decimal(row[value_idx].strip().replace(",", "."))
        return diagnostic_year, values_dict, Diagnostic.DiagnosticType.SIMPLE
