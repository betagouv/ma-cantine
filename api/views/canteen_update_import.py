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

from .canteen import AddManagerView
from .utils import camelize


CANTEEN_UPDATE_SCHEMA_FILE_NAME = "cantines_modifier.json"
CANTEEN_UPDATE_SCHEMA_FILE_PATH = f"data/schemas/imports/{CANTEEN_UPDATE_SCHEMA_FILE_NAME}"
CANTEEN_UPDATE_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{CANTEEN_UPDATE_SCHEMA_FILE_PATH}"


class CanteensUpdateImportView(BaseImportView):
    import_type = ImportType.CANTEEN_UPDATE
    model_class = Canteen

    manager_column_idx = 14  # gestionnaires_additionnels

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canteens_updated = {}

    def _get_schema_config(self):
        """Return schema config"""
        return {
            "name": CANTEEN_UPDATE_SCHEMA_FILE_NAME,
            "url": CANTEEN_UPDATE_SCHEMA_URL,
            "path": CANTEEN_UPDATE_SCHEMA_FILE_PATH,
        }

    def _process_file(self, data):
        """Process file"""
        for row_number, row in enumerate(data, start=1):
            if row_number == 1:  # skip header
                continue
            try:
                canteen = self._save_data_from_row(row)
                self.canteens_updated[canteen.siret] = canteen

            except Exception as e:
                identifier = row[0] if row else None
                for error in self._parse_errors(e, row, identifier):
                    self.errors.append(self._get_error(e, error["message"], error["code"], row_number))

    @transaction.atomic
    def _save_data_from_row(self, row):
        """Process and save canteen data from row"""
        manager_emails = self._get_manager_emails_to_notify(row)
        canteen = self._update_canteen(row, manager_emails)
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
            else [camelize(FullCanteenSerializer(canteen).data) for canteen in self.canteens_updated.values()]
        )
        return {
            "canteens": serialized_canteens,
            "count": len(serialized_canteens),
        }

    def _get_manager_emails_to_notify(self, row):
        try:
            manager_emails = []
            if len(row) > self.manager_column_idx and row[self.manager_column_idx]:
                manager_emails = CanteensUpdateImportView._get_manager_emails(row[self.manager_column_idx])
        except Exception:
            raise ValidationError(
                {"email": f"Un adresse email des gestionnaires ({row[self.manager_column_idx]}) n'est pas valide."}
            )
        return manager_emails

    def _update_canteen(
        self,
        row,
        manager_emails,
    ):
        id = row[0]

        # ID : check canteen exists
        canteen = Canteen.objects.get(id=id)
        if not canteen:
            raise ValidationError(
                {"id": f"Aucune cantine avec le numéro identifiant « {id} » trouvée sur la plateforme."}
            )

        siret = utils_utils.normalize_string(row[1]) if row[1] else None
        siren_unite_legale = utils_utils.normalize_string(row[2]) if row[2] else None
        name = row[3].strip()

        city_insee_code = utils_utils.normalize_string(row[4]) if row[4] else None
        # Validate city_insee_code
        if siren_unite_legale and city_insee_code:
            if len(city_insee_code) != 5:
                raise ValidationError(
                    {
                        "city_insee_code": f"Le code INSEE « {city_insee_code} » n'est pas valide, il doit contenir 5 caractères (ex : 75056)."
                    }
                )

        central_producer_siret = utils_utils.normalize_string(row[5]) if row[5] else None
        daily_meal_count = row[6]
        yearly_meal_count = row[7]
        sector_list = [
            next(value for value, label in Sector.choices if label == sector.strip().replace("’", "'"))
            for sector in row[8].strip().split(",")
        ]
        production_type = next(
            (value for value, label in Canteen.ProductionType.choices if row[9].strip() in [label, value]), None
        )
        management_type = next(
            (value for value, label in Canteen.ManagementType.choices if row[10].strip() in [label, value]), None
        )
        economic_model = next(
            (value for value, label in Canteen.EconomicModel.choices if row[11].strip() in [label, value]), None
        )

        # Group custom validation
        groupe_id = row[12]
        groupe = None
        if groupe_id:
            try:
                groupe = Canteen.objects.get(id=groupe_id)
            except Exception:
                raise ValidationError(
                    {"groupe_id": f"Aucun groupe avec le numéro identifiant « {groupe_id} » trouvé sur la plateforme."}
                )

        line_ministry = (
            next((value for value, label in Canteen.Ministries.choices if label == row[13].strip()), None)
            if row[13]
            else None
        )

        if canteen and not self._has_canteen_permission(canteen):
            raise PermissionDenied(detail="Vous n'êtes pas un gestionnaire de cette cantine.")

        canteen.siret = siret
        canteen.siren_unite_legale = siren_unite_legale
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

        # Need to first update the canteen because when the SIRET is changing to SIREN it will not save the city_insee_code
        if siren_unite_legale and city_insee_code:
            canteen.city_insee_code = city_insee_code
        canteen.save()

        update_change_reason(canteen, f"Mass CSV import. {self.__class__.__name__[:100]}")

        if manager_emails:
            CanteensUpdateImportView._add_managers_to_canteen(manager_emails, canteen)

        return canteen

    def _get_generic_error_message(self):
        return "Une erreur s'est produite en modifiant une cantine pour cette ligne"
