from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction

from api.serializers import FullCanteenSerializer
from api.views.base_import import BaseImportView
from data.models import Canteen, ImportType

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
        # TODO: Implement update canteen logic
        pass

    def _get_generic_error_message(self):
        return "Une erreur s'est produite en modifiant une cantine pour cette ligne"
