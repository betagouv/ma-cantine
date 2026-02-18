from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from rest_framework.exceptions import PermissionDenied
from simple_history.utils import update_change_reason

from api.serializers import FullCanteenSerializer
from api.views.base_import import BaseImportView
from common.utils import utils as utils_utils
from data.models import Canteen, ImportType, Sector
from data.models.creation_source import CreationSource

from .canteen import AddManagerView
from .utils import camelize


CANTEEN_SCHEMA_FILE_NAME = "cantines.json"
CANTEEN_SCHEMA_FILE_PATH = f"data/schemas/imports/{CANTEEN_SCHEMA_FILE_NAME}"
CANTEEN_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{CANTEEN_SCHEMA_FILE_PATH}"


class CanteensCreateImportView(BaseImportView):
    import_type = ImportType.CANTEEN_ONLY
    model_class = Canteen

    manager_column_idx = 11  # gestionnaires_additionnels

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canteens_created = {}

    def _get_schema_config(self):
        """Return schema config based on user role"""
        return {
            "name": CANTEEN_SCHEMA_FILE_NAME,
            "url": CANTEEN_SCHEMA_URL,
            "path": CANTEEN_SCHEMA_FILE_PATH,
        }

    def _process_file(self, data):
        """Process file and track canteens needing geolocation"""
        for row_number, row in enumerate(data, start=1):
            if row_number == 1:  # skip header
                continue
            try:
                canteen = self._save_data_from_row(row)
                self.canteens_created[canteen.siret] = canteen

            except Exception as e:
                identifier = row[0] if row else None
                for error in self._parse_errors(e, row, identifier):
                    self.errors.append(self._get_error(e, error["message"], error["code"], row_number))

    @transaction.atomic
    def _save_data_from_row(self, row):
        """Process and save canteen data from row"""
        manager_emails = self._get_manager_emails_to_notify(row)
        canteen = self._update_or_create_canteen(row, manager_emails)
        return canteen

    @staticmethod
    def _get_manager_emails(row):
        manager_emails = row.split(",")
        normalized_emails = list(map(lambda x: get_user_model().objects.normalize_email(x.strip()), manager_emails))
        for email in normalized_emails:
            validate_email(email)
        return normalized_emails

    @staticmethod
    def _add_managers_to_canteen(emails, canteen):
        for email in emails:
            try:
                AddManagerView.add_manager_to_canteen(email, canteen, send_invitation_mail=True)
            except IntegrityError:
                pass

    def _get_response_data(self):
        """Return canteen-specific response data"""
        serialized_canteens = (
            []
            if self.errors
            else [camelize(FullCanteenSerializer(canteen).data) for canteen in self.canteens_created.values()]
        )
        return {
            "canteens": serialized_canteens,
            "count": len(serialized_canteens),
        }

    def _get_manager_emails_to_notify(self, row):
        try:
            manager_emails = []
            if len(row) > self.manager_column_idx and row[self.manager_column_idx]:
                manager_emails = CanteensCreateImportView._get_manager_emails(row[self.manager_column_idx])
        except Exception:
            raise ValidationError(
                {"email": f"Un adresse email des gestionnaires ({row[self.manager_column_idx]}) n'est pas valide."}
            )
        return manager_emails

    def _update_or_create_canteen(
        self,
        row,
        manager_emails,
    ):
        # TODO: remove hardcoded indexes
        siret = utils_utils.normalize_string(row[0])
        name = row[1].strip()
        central_producer_siret = utils_utils.normalize_string(row[2]) if row[2] else None
        daily_meal_count = row[3]
        yearly_meal_count = row[4]
        sector_list = [
            next(value for value, label in Sector.choices if label == sector.strip().replace("’", "'"))
            for sector in row[5].strip().split(",")
        ]
        production_type = next(
            (value for value, label in Canteen.ProductionType.choices if row[6].strip() in [label, value]), None
        )
        management_type = next(
            (value for value, label in Canteen.ManagementType.choices if row[7].strip() in [label, value]), None
        )
        economic_model = next(
            (value for value, label in Canteen.EconomicModel.choices if row[8].strip() in [label, value]), None
        )

        # Group custom validation
        groupe_id = row[9]
        groupe = None
        if groupe_id:
            try:
                groupe = Canteen.objects.get(id=groupe_id)
            except Exception:
                raise ValidationError(
                    {"groupe_id": f"Aucun groupe avec le numéro identifiant « {groupe_id} » trouvé sur la plateforme."}
                )

        line_ministry = (
            next((value for value, label in Canteen.Ministries.choices if label == row[10].strip()), None)
            if row[10]
            else None
        )

        canteen_exists = Canteen.objects.filter(siret=siret).exists()
        canteen = (
            Canteen.objects.get(siret=siret)
            if canteen_exists
            else Canteen.objects.create(
                name=name,
                siret=siret,
                daily_meal_count=daily_meal_count,
                yearly_meal_count=yearly_meal_count,
                sector_list=sector_list,
                management_type=management_type,
                production_type=production_type,
                economic_model=economic_model,
                central_producer_siret=central_producer_siret,
                groupe=groupe,
                line_ministry=line_ministry,
                creation_source=CreationSource.IMPORT,
            )
        )

        if not canteen_exists:
            update_change_reason(canteen, f"Mass CSV import - canteen creation. {self.__class__.__name__[:100]}")

        if canteen_exists and not self._has_canteen_permission(canteen):
            raise PermissionDenied(detail="Vous n'êtes pas un gestionnaire de cette cantine.")

        canteen.name = name
        canteen.daily_meal_count = daily_meal_count
        canteen.yearly_meal_count = yearly_meal_count
        canteen.sector_list = sector_list
        canteen.production_type = production_type
        canteen.management_type = management_type
        canteen.economic_model = economic_model
        canteen.central_producer_siret = central_producer_siret
        canteen.groupe = groupe
        canteen.line_ministry = line_ministry

        canteen.save()
        update_change_reason(canteen, f"Mass CSV import. {self.__class__.__name__[:100]}")

        canteen.managers.add(self.request.user)
        if manager_emails:
            CanteensCreateImportView._add_managers_to_canteen(manager_emails, canteen)
        return canteen

    def _parse_errors(self, e, row, identifier=None):
        """Extended error parsing for canteen-specific errors"""
        errors = []

        # Handle canteen-specific exceptions first
        if isinstance(e, Canteen.MultipleObjectsReturned):
            self._add_error(
                errors,
                f"Plusieurs cantines correspondent au SIRET {identifier}. Veuillez enlever les doublons.",
            )
            return errors
        elif isinstance(e, FileFormatError):
            self._add_error(errors, e.detail)
            return errors

        # Fall back to base class handling
        return super()._parse_errors(e, row, identifier)

    def _get_generic_error_message(self):
        return "Une erreur s'est produite en créant une cantine pour cette ligne"


class FileFormatError(Exception):
    def __init__(self, detail, **kwargs):
        self.detail = detail
        super().__init__(detail)
