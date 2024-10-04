import csv
import logging
import re
import time
from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from django.db.models.functions import Lower
from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from simple_history.utils import update_change_reason

from api.permissions import IsAuthenticated
from api.serializers import FullCanteenSerializer
from data.models import Canteen, ImportFailure, ImportType, Sector
from data.models.diagnostic import Diagnostic
from data.models.teledeclaration import Teledeclaration

from .canteen import AddManagerView
from .utils import camelize, decode_bytes, normalise_siret

logger = logging.getLogger(__name__)


class ImportDiagnosticsView(ABC, APIView):
    permission_classes = [IsAuthenticated]
    value_error_regex = re.compile(r"Field '(.+)' expected .+? got '(.+)'.")
    annotated_sectors = Sector.objects.annotate(name_lower=Lower("name"))
    manager_column_idx = 11
    year_idx = 12

    def __init__(self, **kwargs):
        self.diagnostics_created = 0
        self.teledeclarations = 0
        self.canteens = {}
        self.errors = []
        self.start_time = None
        self.encoding_detected = None
        self.file = None
        super().__init__(**kwargs)

    @property
    @abstractmethod
    def final_value_idx(): ...

    @property
    @abstractmethod
    def import_type(): ...

    def post(self, request):
        self.start_time = time.time()
        logger.info("Diagnostic bulk import started")
        try:
            with transaction.atomic():
                self.file = request.data["file"]
                ImportDiagnosticsView._verify_file_format(self.file)
                ImportDiagnosticsView._verify_file_size(self.file)
                self._treat_csv_file(self.file)

                if self.errors:
                    raise IntegrityError()
        except IntegrityError as e:
            self._log_error(f"L'import du fichier CSV a échoué:\n{e}")
        except ValidationError as e:
            self._log_error(e.message)
            self.errors = [{"row": 0, "status": 400, "message": e.message}]
        except UnicodeDecodeError as e:
            self._log_error(e.reason)
            self.errors = [{"row": 0, "status": 400, "message": "Le fichier doit être sauvegardé en Unicode (utf-8)"}]
        except Exception as e:
            self._log_error(f"Échec lors de la lecture du fichier:\n{e}", "exception")
            self.errors = [{"row": 0, "status": 400, "message": "Échec lors de la lecture du fichier"}]

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

    @staticmethod
    def _verify_file_format(file):
        if file.content_type != "text/csv" and file.content_type != "text/tab-separated-values":
            raise ValidationError(
                f"Ce fichier est du format {file.content_type}, merci d'exporter votre fichier en format CSV et re-essayer."
            )

    @staticmethod
    def _verify_file_size(file):
        if file.size > settings.CSV_IMPORT_MAX_SIZE:
            raise ValidationError("Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo")

    def _treat_csv_file(self, file):
        locations_csv_str = "siret,citycode,postcode\n"
        has_locations_to_find = False

        filestring = self._decode_file(file)
        filelines = filestring.splitlines()
        dialect = csv.Sniffer().sniff(filelines[0])

        csvreader = csv.reader(filelines, dialect=dialect)
        for row_number, row in enumerate(csvreader, start=1):
            try:
                if self._skip_row(row_number, row):
                    continue
                canteen, should_update_geolocation = self._save_data_from_row(row)
                self.canteens[canteen.siret] = canteen
                if should_update_geolocation:
                    has_locations_to_find = True
                    if canteen.city_insee_code:
                        locations_csv_str += f"{canteen.siret},{canteen.city_insee_code},\n"
                    else:
                        locations_csv_str += f"{canteen.siret},,{canteen.postal_code}\n"

            except Exception as e:
                for error in self._parse_errors(e, row):
                    self.errors.append(
                        ImportDiagnosticsView._get_error(e, error["message"], error["code"], row_number)
                    )
        if has_locations_to_find:
            self._update_location_data(locations_csv_str)

    def _decode_file(self, file):
        (result, encoding) = decode_bytes(file.read())
        self.encoding_detected = encoding
        return result

    @transaction.atomic
    def _save_data_from_row(self, row):
        if row[0] == "":
            raise ValidationError({"siret": "Le siret de la cantine ne peut pas être vide"})
        # validate data for format etc, starting with basic non-data-specific row checks
        self._validate_row(row)
        ImportDiagnosticsView._validate_canteen(row)
        manager_emails = self._get_manager_emails_to_notify(row)
        diagnostic_year, values_dict, diagnostic_type = self._validate_diagnostic(row)
        # return staff-customisable fields
        (
            import_source,
            publication_status,
            should_teledeclare,
            silently_added_manager_emails,
        ) = self._generate_canteen_meta_fields(row)
        # create the canteen and potentially the diagnostic
        canteen, should_update_geolocation = self._update_or_create_canteen(
            row, import_source, publication_status, manager_emails, silently_added_manager_emails
        )
        if diagnostic_year:
            diagnostic = self._update_or_create_diagnostic(canteen, diagnostic_year, values_dict, diagnostic_type)
            if should_teledeclare and self.request.user.is_staff:
                self._teledeclare_diagnostic(diagnostic)

        return (canteen, should_update_geolocation)

    @abstractmethod
    def _skip_row(self, row_number, row): ...

    @abstractmethod
    def _validate_row(self, row): ...

    @abstractmethod
    def _validate_diagnostic(self, row): ...

    # NB: this function should only be called once the data has been validated since by this point a canteen
    # will have been saved to the DB and we don't want partial imports caused by exceptions from this method
    def _update_or_create_diagnostic(self, canteen, diagnostic_year, values_dict, diagnostic_type):
        diagnostic_exists = Diagnostic.objects.filter(canteen=canteen, year=diagnostic_year).exists()
        diagnostic = (
            Diagnostic.objects.get(canteen=canteen, year=diagnostic_year)
            if diagnostic_exists
            else Diagnostic(canteen_id=canteen.id, year=diagnostic_year)
        )
        if diagnostic_exists:
            has_active_td = Teledeclaration.objects.filter(
                diagnostic=diagnostic, status=Teledeclaration.TeledeclarationStatus.SUBMITTED
            ).exists()
            if has_active_td:
                raise ValidationError(
                    "Ce n'est pas possible de modifier un diagnostic télédéclaré. Veuillez retirer cette ligne, ou annuler la télédéclaration."
                )
        diagnostic.diagnostic_type = diagnostic_type
        for key, value in values_dict.items():
            setattr(diagnostic, key, value)
        diagnostic.full_clean()
        diagnostic.save()
        update_change_reason(diagnostic, f"Mass CSV import. {self.__class__.__name__[:100]}")
        self.diagnostics_created += 1
        return diagnostic

    def _teledeclare_diagnostic(self, diagnostic):
        Teledeclaration.validate_diagnostic(diagnostic)
        try:
            Teledeclaration.create_from_diagnostic(diagnostic, self.request.user)
            self.teledeclarations += 1
        except Exception:
            raise ValidationError("Ce diagnostic n'a pas été télédéclaré")

    @staticmethod
    def _should_update_geolocation(canteen, row):
        if canteen.city:
            city_code_changed = row[2] and canteen.city_insee_code != row[2].strip()
            postal_code_changed = row[3] and canteen.postal_code != row[3].strip()
            return city_code_changed or postal_code_changed
        else:
            has_geo_data = canteen.city_insee_code or canteen.postal_code
            return has_geo_data

    @staticmethod
    def _get_error(e, message, error_status, row_number):
        logger.exception(f"Error on row {row_number}:\n{e}")
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

    @staticmethod
    def _get_manager_emails(row):
        manager_emails = row.split(",")
        normalized_emails = list(map(lambda x: get_user_model().objects.normalize_email(x.strip()), manager_emails))
        for email in normalized_emails:
            validate_email(email)
        return normalized_emails

    @staticmethod
    def _add_managers_to_canteen(emails, canteen, send_invitation_mail=True):
        for email in emails:
            try:
                AddManagerView.add_manager_to_canteen(email, canteen, send_invitation_mail=send_invitation_mail)
            except IntegrityError as e:
                logger.warning(
                    f"Attempt to add existing manager with email {email} to canteen {canteen.id} from a CSV import:\n{e}"
                )

    def _get_success_response(self):
        serialized_canteens = (
            []
            if len(self.errors)
            else [camelize(FullCanteenSerializer(canteen).data) for canteen in self.canteens.values()]
        )
        body = {
            "canteens": serialized_canteens,
            "count": 0 if len(self.errors) else self.diagnostics_created,
            "errors": self.errors,
            "seconds": time.time() - self.start_time,
            "encoding": self.encoding_detected,
        }
        if self.request.user.is_staff:
            body["teledeclarations"] = self.teledeclarations
        return JsonResponse(body, status=status.HTTP_200_OK)

    def _update_location_data(self, locations_csv_str):
        try:
            # NB: max size of a csv file is 50 MB
            response = requests.post(
                "https://api-adresse.data.gouv.fr/search/csv/",
                files={
                    "data": ("locations.csv", locations_csv_str),
                },
                data={
                    "postcode": "postcode",
                    "citycode": "citycode",
                    "result_columns": ["result_citycode", "result_postcode", "result_city", "result_context"],
                },
                timeout=4,
            )
            response.raise_for_status()  # Raise an exception if the request failed
            for row in csv.reader(response.text.splitlines()):
                if row[0] == "siret":
                    continue  # skip header
                if row[5] != "":  # city found, so rest of data is found
                    canteen = self.canteens[row[0]]
                    canteen.city_insee_code = row[3]
                    canteen.postal_code = row[4]
                    canteen.city = row[5]
                    canteen.department = row[6].split(",")[0]
                    canteen.save()
                    update_change_reason(canteen, f"Mass CSV import - Geo data. {self.__class__.__name__[:100]}")
        except Exception as e:
            logger.exception(f"Error while updating location data : {repr(e)} - {e}")

    @staticmethod
    def _add_error(errors, message, code=400):
        errors.append({"message": message, "code": code})

    @staticmethod
    def _validate_canteen(row):
        if not normalise_siret(row[0]).isdigit():
            raise ValidationError({"siret": "Le SIRET doit être composé des chiffres"})
        if not row[5]:
            raise ValidationError({"daily_meal_count": "Ce champ ne peut pas être vide."})
        if not row[5].strip().isdigit():
            raise ValidationError({"daily_meal_count": f"La valeur « {row[5]} » doit être un nombre entier."})
        if not row[6]:
            raise ValidationError({"yearly_meal_count": "Ce champ ne peut pas être vide."})
        if not row[6].strip().isdigit():
            raise ValidationError({"yearly_meal_count": f"La valeur « {row[6]} » doit être un nombre entier."})
        elif not row[2] and not row[3]:
            raise ValidationError(
                {"postal_code": "Ce champ ne peut pas être vide si le code INSEE de la ville est vide."}
            )
        if row[4]:
            central_producer_siret = normalise_siret(row[4])
            siret = normalise_siret(row[0])
            if central_producer_siret == siret:
                raise ValidationError(
                    {
                        "central_producer_siret": "Le SIRET de la cuisine centrale doit être différent de celui de la cantine"
                    }
                )

    def _get_manager_emails_to_notify(self, row):
        try:
            manager_emails = []
            if len(row) > self.manager_column_idx + 1 and row[self.manager_column_idx]:
                manager_emails = ImportDiagnosticsView._get_manager_emails(row[self.manager_column_idx])
        except Exception:
            raise ValidationError(
                {"email": f"Un adresse email des gestionnaires ({row[self.manager_column_idx]}) n'est pas valide."}
            )
        return manager_emails

    def _has_canteen_permission(self, canteen):
        return self.request.user in canteen.managers.all()

    def _update_or_create_canteen(
        self,
        row,
        import_source,
        publication_status,
        manager_emails,
        silently_added_manager_emails,
        satellite_canteens_count=None,
    ):
        siret = normalise_siret(row[0])
        canteen_exists = Canteen.objects.filter(siret=siret).exists()
        canteen = Canteen.objects.get(siret=siret) if canteen_exists else Canteen.objects.create(siret=siret)

        if not canteen_exists:
            update_change_reason(canteen, f"Mass CSV import - canteen creation. {self.__class__.__name__[:100]}")

        if canteen_exists and not self._has_canteen_permission(canteen):
            raise PermissionDenied(detail="Vous n'êtes pas un gestionnaire de cette cantine.")

        should_update_geolocation = (
            ImportDiagnosticsView._should_update_geolocation(canteen, row) if canteen_exists else True
        )

        canteen.name = row[1].strip()
        canteen.city_insee_code = row[2].strip()
        canteen.postal_code = row[3].strip()
        canteen.central_producer_siret = normalise_siret(row[4])
        canteen.daily_meal_count = row[5].strip()
        canteen.yearly_meal_count = row[6].strip()
        canteen.production_type = row[8].strip().lower()
        canteen.management_type = row[9].strip().lower()
        canteen.economic_model = row[10].strip().lower() if len(row) > 10 else None
        canteen.import_source = import_source
        canteen.publication_status = publication_status
        if satellite_canteens_count:
            canteen.satellite_canteens_count = satellite_canteens_count

        # full_clean must be before the relation-model updates bc they don't require a save().
        # If an exception is launched by full_clean, it must be here.
        canteen.full_clean()
        if row[7]:
            canteen.sectors.set(
                [
                    self.annotated_sectors.get(name_lower__unaccent=sector.strip().lower())
                    for sector in row[7].split("+")
                ]
            )

        canteen.save()
        update_change_reason(canteen, f"Mass CSV import. {self.__class__.__name__[:100]}")

        if not self.request.user.is_staff:
            canteen.managers.add(self.request.user)
        if manager_emails:
            ImportDiagnosticsView._add_managers_to_canteen(manager_emails, canteen)
        if silently_added_manager_emails:
            ImportDiagnosticsView._add_managers_to_canteen(
                silently_added_manager_emails, canteen, send_invitation_mail=False
            )
        return (canteen, should_update_geolocation)

    def _generate_canteen_meta_fields(self, row):
        silent_manager_idx = self.final_value_idx + 1
        silently_added_manager_emails = []
        import_source = "Import massif"
        publication_status = Canteen.PublicationStatus.DRAFT
        should_teledeclare = False
        if len(row) > silent_manager_idx:  # already checked earlier that it's a staff user
            try:
                if row[silent_manager_idx]:
                    silently_added_manager_emails = ImportDiagnosticsView._get_manager_emails(row[silent_manager_idx])
            except Exception:
                raise ValidationError(
                    {
                        "email": f"Un adresse email des gestionnaires (pas notifiés) ({row[silent_manager_idx]}) n'est pas valide."
                    }
                )

            try:
                import_source = row[silent_manager_idx + 1].strip()
            except Exception:
                raise ValidationError({"import_source": "Ce champ ne peut pas être vide."})

            status_idx = silent_manager_idx + 2
            if len(row) > status_idx and row[status_idx]:
                publication_status = row[status_idx].strip()
            teledeclaration_idx = silent_manager_idx + 3
            if len(row) > teledeclaration_idx and row[teledeclaration_idx]:
                if row[teledeclaration_idx] != "teledeclared":
                    raise ValidationError(
                        {
                            "teledeclaration": f"'{row[teledeclaration_idx]}' n'est pas un statut de télédéclaration valid"
                        }
                    )
                should_teledeclare = True
        return (import_source, publication_status, should_teledeclare, silently_added_manager_emails)

    def _parse_errors(self, e, row):  # noqa: C901
        errors = []
        if isinstance(e, PermissionDenied):
            ImportDiagnosticsView._add_error(errors, e.detail, 401)
        elif isinstance(e, Sector.DoesNotExist):
            ImportDiagnosticsView._add_error(errors, "Le secteur spécifié ne fait pas partie des options acceptées")
        elif isinstance(e, ValidationError):
            if hasattr(e, "message_dict"):
                for field, messages in e.message_dict.items():
                    verbose_field_name = ImportDiagnosticsView._get_verbose_field_name(field)
                    for message in messages:
                        user_message = message
                        if field != "__all__":
                            user_message = f"Champ '{verbose_field_name}' : {user_message}"
                        ImportDiagnosticsView._add_error(errors, user_message)
            elif hasattr(e, "message"):
                ImportDiagnosticsView._add_error(errors, e.message)
            elif hasattr(e, "params"):
                ImportDiagnosticsView._add_error(errors, f"La valeur '{e.params['value']}' n'est pas valide.")
            else:
                logger.exception(f"Unknown validation error: {e}")
                ImportDiagnosticsView._add_error(
                    errors, "Une erreur s'est produite en créant un diagnostic pour cette ligne"
                )
        elif isinstance(e, ValueError):
            match = self.value_error_regex.search(str(e))
            field_name = match.group(1) if match else ""
            value_given = match.group(2) if match else ""
            if field_name:
                verbose_field_name = ImportDiagnosticsView._get_verbose_field_name(field_name)
                ImportDiagnosticsView._add_error(
                    errors, f"La valeur '{value_given}' n'est pas valide pour le champ '{verbose_field_name}'."
                )
        elif isinstance(e, IndexError):
            ImportDiagnosticsView._add_error(errors, self._column_count_error_message(row))
        elif isinstance(e, Canteen.MultipleObjectsReturned):
            ImportDiagnosticsView._add_error(
                errors,
                f"Plusieurs cantines correspondent au SIRET {row[0]}. Veuillez enlever les doublons pour pouvoir créer le diagnostic.",
            )
        elif isinstance(e, FileFormatError):
            ImportDiagnosticsView._add_error(errors, e.detail)
        if not errors:
            logger.exception(f"No errors added through parsing but exception raised: {e}")
            ImportDiagnosticsView._add_error(
                errors, "Une erreur s'est produite en créant un diagnostic pour cette ligne"
            )
        return errors

    @abstractmethod
    def _column_count_error_message(self, row): ...


# Allows canteen-only and simple diagnostics import
class ImportSimpleDiagnosticsView(ImportDiagnosticsView):
    final_value_idx = 22
    total_value_idx = 13
    import_type = ImportType.CANTEEN_ONLY_OR_DIAGNOSTIC_SIMPLE

    def _skip_row(self, row_number, row):
        return row_number == 1 and row[0].lower() == "siret"

    def _validate_row(self, row):
        # manager column isn't required, neither is the economic_model. so intentionally checking less than that idx - 1
        last_mandatory_column = self.manager_column_idx - 1
        if len(row) < last_mandatory_column:
            raise IndexError()
        elif len(row) > self.year_idx and len(row) < self.total_value_idx + 1:
            raise IndexError()
        elif len(row) > self.final_value_idx + 1 and not self.request.user.is_staff:
            raise PermissionDenied(
                detail=f"Format fichier : {self.final_value_idx + 1} ou 12 colonnes attendues, {len(row)} trouvées."
            )
        try:
            diagnostic_year = row[self.year_idx]
            # Flake formatting bug: https://github.com/PyCQA/pycodestyle/issues/373#issuecomment-760190686
            if not diagnostic_year and any(row[13 : self.final_value_idx]):  # noqa: E203
                raise ValidationError({"year": "L'année est obligatoire pour créer un diagnostic."})
        except IndexError:
            pass

    def _validate_diagnostic(self, row):
        # NB: if year is given, appro data is required, else only canteen data required
        values_dict = None
        diagnostic_year = row[self.year_idx] if len(row) > self.year_idx else None

        if diagnostic_year:
            try:
                diagnostic_year = int(diagnostic_year.strip())
            except ValueError:
                raise ValidationError({"year": f"La valeur « {row[self.year_idx]} » doit être un nombre entier."})
            mandatory_fields = [
                "value_total_ht",
            ]
            value_fields = [
                "value_total_ht",
                "value_bio_ht",
                "value_sustainable_ht",
                "value_externality_performance_ht",
                "value_egalim_others_ht",
                "value_meat_poultry_ht",
                "value_meat_poultry_egalim_ht",
                "value_meat_poultry_france_ht",
                "value_fish_ht",
                "value_fish_egalim_ht",
            ]
            appro_fields_length = len(row) - self.total_value_idx
            value_fields = value_fields[:appro_fields_length]
            values_dict = {}
            value_offset = 0
            for value in value_fields:
                value_offset = value_offset + 1
                value_idx = self.year_idx + value_offset
                if value in mandatory_fields and not row[value_idx]:
                    error = {}
                    error[value] = "Ce champ ne peut pas être vide."
                    raise ValidationError(error)
                try:
                    values_dict[value] = (
                        None if not row[value_idx] else Decimal(row[value_idx].strip().replace(",", "."))
                    )
                except InvalidOperation:
                    error = {}
                    # TODO: This should take into account more number formats and be factored out to utils
                    error[value] = f"La valeur « {row[value_idx]} » doit être un nombre décimal."
                    raise ValidationError(error)
        return diagnostic_year, values_dict, Diagnostic.DiagnosticType.SIMPLE

    def _column_count_error_message(self, row):
        return f"Données manquantes : 23 colonnes attendues, {len(row)} trouvées."


class ImportCompleteDiagnosticsView(ImportDiagnosticsView):
    final_value_idx = 127
    import_type = ImportType.DIAGNOSTIC_COMPLETE

    def _skip_row(self, row_number, row):
        if row_number == 1:
            message = "Deux lignes en-tête attendues, {} trouvée. Veuillez vérifier que vous voulez importer les diagnostics complets, et assurez-vous que le format de l'en-tête suit les exemples donnés."
            if row[0] and row[0].lower() == "siret":
                raise FileFormatError(detail=message.format(1))
            elif row[0]:
                # making the grand assumption that anything other than "SIRET" resembles a siret number
                raise FileFormatError(detail=message.format(0))
            return True
        elif row_number == 2:
            return True

    def _validate_row(self, row):
        # complete diagnostic should at least have the year and total
        if len(row) < self.year_idx + 1:
            raise IndexError()
        elif len(row) > self.final_value_idx + 1:
            raise FileFormatError(
                detail=f"Format fichier : {self.final_value_idx + 1} colonnes attendues, {len(row)} trouvées."
            )

    def _validate_diagnostic(self, row):
        try:
            diagnostic_year = int(row[self.year_idx].strip())
        except Exception:
            raise ValidationError(
                {
                    "year": "Ce champ doit être un nombre entier. Si vous voulez importer que la cantine, veuillez changer le type d'import et réessayer."
                }
            )
        values_dict = {}
        value_idx = self.year_idx + 1
        # total value is required, handle this case separately to the remaining values which are optional
        try:
            values_dict["value_total_ht"] = Decimal(row[value_idx].strip().replace(",", "."))
        except InvalidOperation:
            raise ValidationError({"value_total_ht": "Ce champ ne peut pas être vide."})
        for value in ["value_meat_poultry_ht", "value_fish_ht", *Diagnostic.complete_fields]:
            try:
                value_idx = value_idx + 1
                if row[value_idx]:
                    values_dict[value] = Decimal(row[value_idx].strip().replace(",", "."))
            except IndexError:
                # we allow the rest of the fields to be left unspecified because there are so many
                break
            except InvalidOperation:
                error = {}
                error[value] = f"La valeur « {row[value_idx]} » doit être vide ou un nombre décimal."
                raise ValidationError(error)
        return diagnostic_year, values_dict, Diagnostic.DiagnosticType.COMPLETE

    def _generate_canteen_meta_fields(self, row):
        return ("Import massif", Canteen.PublicationStatus.DRAFT, False, [])

    def _column_count_error_message(self, row):
        return f"Données manquantes : au moins 13 colonnes attendues, {len(row)} trouvées. Si vous voulez importer que la cantine, veuillez changer le type d'import et réessayer."


class CCImportMixin:
    total_value_idx = 14
    year_idx = 13
    cc_satellite_dict = {}

    def _validate_row(self, row):
        is_central_kitchen = CCImportMixin._is_central_kitchen(row)
        last_mandatory_column = self.manager_column_idx - 1

        if is_central_kitchen:
            if len(row) < self.year_idx + 1:
                raise IndexError()
            elif len(row) > self.final_value_idx + 1:
                raise FileFormatError(
                    detail=f"Format fichier : {self.final_value_idx + 1} colonnes attendues, {len(row)} trouvées."
                )

        elif len(row) < last_mandatory_column:
            raise IndexError()

    def _treat_csv_file(self, file):
        return_value = super()._treat_csv_file(file)
        self._clean_removed_satellites()
        return return_value

    def _clean_removed_satellites(self):
        for central_cuisine_siret in self.cc_satellite_dict:
            satellite_sirets = self.cc_satellite_dict[central_cuisine_siret]
            canteens_to_remove = Canteen.objects.filter(central_producer_siret=central_cuisine_siret).exclude(
                siret__in=satellite_sirets
            )
            canteens_to_remove.update(central_producer_siret=None)
            for canteen in canteens_to_remove:
                update_change_reason(canteen, f"Mass CSV import - unlinking CC. {self.__class__.__name__[:100]}")

    def _validate_diagnostic(self, row):
        is_central_kitchen = CCImportMixin._is_central_kitchen(row)
        if is_central_kitchen:
            return super()._validate_diagnostic(row)
        return None, None, None

    def _update_or_create_canteen(
        self,
        row,
        import_source,
        publication_status,
        manager_emails,
        silently_added_manager_emails,
        satellite_canteens_count=None,
    ):
        is_central_kitchen = CCImportMixin._is_central_kitchen(row)
        if is_central_kitchen:
            satellite_canteens_count = row[12].strip()
        return super()._update_or_create_canteen(
            row,
            import_source,
            publication_status,
            manager_emails,
            silently_added_manager_emails,
            satellite_canteens_count,
        )

    @staticmethod
    def _is_central_kitchen(row):
        production_type = row[8].strip().lower()
        return (
            production_type == Canteen.ProductionType.CENTRAL.value
            or production_type == Canteen.ProductionType.CENTRAL_SERVING.value
        )

    def _save_data_from_row(self, row):
        canteen, should_update_geolocation = super()._save_data_from_row(row)
        if CCImportMixin._is_central_kitchen(row) and canteen.siret not in self.cc_satellite_dict:
            self.cc_satellite_dict[canteen.siret] = []
        else:
            if canteen.central_producer_siret in self.cc_satellite_dict:
                self.cc_satellite_dict[canteen.central_producer_siret].append(canteen.siret)
            else:
                self.cc_satellite_dict[canteen.central_producer_siret] = [canteen.siret]
        return (canteen, should_update_geolocation)


class ImportSimpleCentralKitchenView(CCImportMixin, ImportSimpleDiagnosticsView):
    final_value_idx = 23
    import_type = ImportType.CC_SIMPLE

    def _column_count_error_message(self, row):
        return f"Données manquantes : 24 colonnes attendues, {len(row)} trouvées."


class ImportCompleteCentralKitchenView(CCImportMixin, ImportCompleteDiagnosticsView):
    final_value_idx = 128
    import_type = ImportType.CC_COMPLETE

    def _column_count_error_message(self, row):
        return f"Données manquantes : au moins 129 colonnes attendues, {len(row)} trouvées. Si vous voulez importer que la cantine, veuillez changer le type d'import et réessayer."


class FileFormatError(Exception):
    def __init__(self, detail, **kwargs):
        self.detail = detail
        super().__init__(detail)
