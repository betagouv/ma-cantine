from abc import ABC, abstractmethod
import csv
import time
import re
import logging
from decimal import Decimal
from data.models.diagnostic import Diagnostic
from data.models.teledeclaration import Teledeclaration
from django.db import IntegrityError, transaction
from django.db.models.functions import Lower
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from api.serializers import FullCanteenSerializer
from data.models import Canteen, Sector
from api.permissions import IsAuthenticated
from .utils import camelize, normalise_siret
from .canteen import AddManagerView
import requests

logger = logging.getLogger(__name__)


class ImportDiagnosticsView(ABC, APIView):
    permission_classes = [IsAuthenticated]
    value_error_regex = re.compile(r"Field '(.+)' expected .+? got '(.+)'.")
    annotated_sectors = Sector.objects.annotate(name_lower=Lower("name"))
    manager_column_idx = 10
    year_idx = 11

    def __init__(self, **kwargs):
        self.diagnostics_created = 0
        self.teledeclarations = 0
        self.canteens = {}
        self.errors = []
        self.start_time = None
        super().__init__(**kwargs)

    @property
    @abstractmethod
    def final_value_idx():
        ...

    def post(self, request):
        self.start_time = time.time()
        logger.info("Diagnostic bulk import started")
        try:
            with transaction.atomic():
                file = request.data["file"]
                ImportDiagnosticsView._verify_file_size(file)
                self._treat_csv_file(file)

                if self.errors:
                    raise IntegrityError()
        except IntegrityError as e:
            logger.warning(f"L'import du fichier CSV a échoué:\n{e}")
        except ValidationError as e:
            message = e.message
            logger.warning(f"{message}")
            self.errors = [{"row": 0, "status": 400, "message": message}]
        except Exception as e:
            logger.exception(f"Échec lors de la lecture du fichier:\n{e}")
            self.errors = [{"row": 0, "status": 400, "message": "Échec lors de la lecture du fichier"}]

        return self._get_success_response()

    @staticmethod
    def _verify_file_size(file):
        if file.size > settings.CSV_IMPORT_MAX_SIZE:
            raise ValidationError("Ce fichier est trop grand, merci d'utiliser un fichier de moins de 10Mo")

    def _treat_csv_file(self, file):
        locations_csv_str = "siret,citycode,postcode\n"
        has_locations_to_find = False

        filestring = file.read().decode("utf-8-sig")
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
            diagnostic = self._create_diagnostic(canteen, diagnostic_year, values_dict, diagnostic_type)
            if should_teledeclare and self.request.user.is_staff:
                self._teledeclare_diagnostic(diagnostic)

        return (canteen, should_update_geolocation)

    @abstractmethod
    def _skip_row(self, row_number, row):
        ...

    @abstractmethod
    def _validate_row(self, row):
        ...

    @abstractmethod
    def _validate_diagnostic(self, row):
        ...

    # NB: this function should only be called once the data has been validated since by this point a canteen
    # will have been saved to the DB and we don't want partial imports caused by exceptions from this method
    def _create_diagnostic(self, canteen, diagnostic_year, values_dict, diagnostic_type):
        diagnostic = Diagnostic(
            canteen_id=canteen.id,
            year=diagnostic_year,
            diagnostic_type=diagnostic_type,
            **values_dict,
        )
        diagnostic.full_clean()
        diagnostic.save()
        self.diagnostics_created += 1
        return diagnostic

    def _teledeclare_diagnostic(self, diagnostic):
        try:
            Teledeclaration.validate_diagnostic(diagnostic)
            Teledeclaration.create_from_diagnostic(diagnostic, self.request.user)
            self.teledeclarations += 1
        except Exception:
            pass

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
        except Exception as e:
            logger.exception(f"Error while updating location data : {repr(e)} - {e}")

    @staticmethod
    def _add_error(errors, message, code=400):
        errors.append({"message": message, "code": code})

    @staticmethod
    def _validate_canteen(row):
        if not row[5]:
            raise ValidationError({"daily_meal_count": "Ce champ ne peut pas être vide."})
        elif not row[2] and not row[3]:
            raise ValidationError(
                {"postal_code": "Ce champ ne peut pas être vide si le code INSEE de la ville est vide."}
            )

    def _get_manager_emails_to_notify(self, row):
        try:
            manager_emails = []
            if len(row) > self.manager_column_idx + 1 and row[self.manager_column_idx]:
                manager_emails = ImportDiagnosticsView._get_manager_emails(row[self.manager_column_idx])
        except Exception:
            raise ValidationError({"email": "Un adresse email des gestionnaires n'est pas valide."})
        return manager_emails

    def _update_or_create_canteen(
        self, row, import_source, publication_status, manager_emails, silently_added_manager_emails
    ):
        siret = normalise_siret(row[0])
        canteen_exists = Canteen.objects.filter(siret=siret).exists()
        canteen = Canteen.objects.get(siret=siret) if canteen_exists else Canteen.objects.create(siret=siret)

        if canteen_exists and self.request.user not in canteen.managers.all():
            raise PermissionDenied(detail="Vous n'êtes pas un gestionnaire de cette cantine.")

        should_update_geolocation = (
            ImportDiagnosticsView._should_update_geolocation(canteen, row) if canteen_exists else True
        )

        canteen.name = row[1].strip()
        canteen.city_insee_code = row[2].strip()
        canteen.postal_code = row[3].strip()
        canteen.central_producer_siret = normalise_siret(row[4])
        canteen.daily_meal_count = row[5].strip()
        canteen.production_type = row[7].strip().lower()
        canteen.management_type = row[8].strip().lower()
        canteen.economic_model = row[9].strip().lower()
        canteen.import_source = import_source
        canteen.publication_status = publication_status

        # full_clean must be before the relation-model updates bc they don't require a save().
        # If an exception is launched by full_clean, it must be here.
        canteen.full_clean()
        if row[6]:
            canteen.sectors.set(
                [
                    self.annotated_sectors.get(name_lower__unaccent=sector.strip().lower())
                    for sector in row[6].split("+")
                ]
            )

        canteen.save()

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
            if e.message_dict:
                for field, messages in e.message_dict.items():
                    verbose_field_name = ImportDiagnosticsView._get_verbose_field_name(field)
                    for message in messages:
                        user_message = message
                        if user_message == "Un objet Diagnostic avec ces champs Canteen et Année existe déjà.":
                            user_message = "Un diagnostic pour cette année et cette cantine existe déjà."
                        if field != "__all__":
                            user_message = f"Champ '{verbose_field_name}' : {user_message}"
                        ImportDiagnosticsView._add_error(errors, user_message)

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
    def _column_count_error_message(self, row):
        ...


# Allows canteen-only and simple diagnostics import
class ImportSimpleDiagnosticsView(ImportDiagnosticsView):
    final_value_idx = 21

    def _skip_row(self, row_number, row):
        return row_number == 1 and row[0].lower() == "siret"

    def _validate_row(self, row):
        # manager column isn't required, so intentionally checking less than that idx
        if len(row) < self.manager_column_idx:
            raise IndexError()
        elif len(row) > self.year_idx and len(row) < self.final_value_idx + 1:
            raise IndexError()
        elif len(row) > self.final_value_idx + 1 and not self.request.user.is_staff:
            raise PermissionDenied(
                detail=f"Format fichier : {self.final_value_idx + 1} ou 11 colonnes attendues, {len(row)} trouvées."
            )

    def _validate_diagnostic(self, row):
        # NB: if year is given, appro data is required, else only canteen data required
        diagnostic_year = values_dict = None
        try:
            diagnostic_year = row[self.year_idx]
            # Flake formatting bug: https://github.com/PyCQA/pycodestyle/issues/373#issuecomment-760190686
            if not diagnostic_year and any(row[12 : self.final_value_idx]):  # noqa: E203
                raise ValidationError({"year": "L'année est obligatoire pour créer un diagnostic."})
        except IndexError:
            pass

        if diagnostic_year:
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
            values_dict = {}
            value_offset = 0
            for value in value_fields:
                try:
                    value_offset = value_offset + 1
                    value_idx = self.year_idx + value_offset
                    if not row[value_idx]:
                        raise Exception
                    values_dict[value] = Decimal(row[value_idx].strip().replace(",", "."))
                except Exception:
                    error = {}
                    # TODO: This should take into account more number formats and be factored out to utils
                    error[value] = "Ce champ doit être un nombre décimal."
                    raise ValidationError(error)
        return diagnostic_year, values_dict, Diagnostic.DiagnosticType.SIMPLE

    def _column_count_error_message(self, row):
        return f"Données manquantes : 22 colonnes attendues, {len(row)} trouvées."


class ImportCompleteDiagnosticsView(ImportDiagnosticsView):
    final_value_idx = 126

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
        except Exception:
            raise ValidationError({"value_total_ht": "Ce champ doit être un nombre décimal."})
        for value in ["value_meat_poultry_ht", "value_fish_ht", *Diagnostic.complete_fields]:
            try:
                value_idx = value_idx + 1
                if row[value_idx]:
                    values_dict[value] = Decimal(row[value_idx].strip().replace(",", "."))
            except IndexError:
                # we allow the rest of the fields to be left unspecified because there are so many
                break
            except Exception:
                error = {}
                error[value] = "Ce champ doit être vide ou un nombre décimal."
                raise ValidationError(error)
        return diagnostic_year, values_dict, Diagnostic.DiagnosticType.COMPLETE

    def _generate_canteen_meta_fields(self, row):
        return ("Import massif", Canteen.PublicationStatus.DRAFT, False, [])

    def _column_count_error_message(self, row):
        return f"Données manquantes : au moins 12 colonnes attendues, {len(row)} trouvées. Si vous voulez importer que la cantine, veuillez changer le type d'import et réessayer."


class FileFormatError(Exception):
    def __init__(self, detail, **kwargs):
        self.detail = detail
        super().__init__(detail)
