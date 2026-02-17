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
from data.models import Canteen, ImportType

from .canteen import AddManagerView
from .utils import camelize


CANTEEN_MANAGERS_SCHEMA_FILE_NAME = "cantines_gestionnaires.json"
CANTEEN_MANAGERS_SCHEMA_FILE_PATH = f"data/schemas/imports/{CANTEEN_MANAGERS_SCHEMA_FILE_NAME}"
CANTEEN_MANAGERS_SCHEMA_URL = f"https://raw.githubusercontent.com/betagouv/ma-cantine/refs/heads/{settings.GIT_BRANCH}/{CANTEEN_MANAGERS_SCHEMA_FILE_PATH}"


class CanteensManagersImportView(BaseImportView):
    import_type = ImportType.CANTEEN_MANAGERS
    model_class = Canteen
    siret_idx = 0
    silent_manager_idx = 1
    source_idx = 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canteens_updated = {}

    def post(self, request):
        self.is_admin = request.user.is_staff
        return super().post(request)

    def _get_schema_config(self):
        """Return schema config based on user role"""
        return {
            "name": CANTEEN_MANAGERS_SCHEMA_FILE_NAME,
            "path": CANTEEN_MANAGERS_SCHEMA_FILE_PATH,
            "url": CANTEEN_MANAGERS_SCHEMA_URL,
        }

    def _process_file(self, data):
        """Process file and add managers without sending invitation emails"""
        if not self.is_admin:
            raise PermissionDenied(
                "Vous n'avez pas les permissions nécessaires pour importer des gestionnaires en masse."
            )

        for row_number, row in enumerate(data, start=1):
            if row_number == 1:  # skip header
                continue
            try:
                canteen = self._save_data_from_row(row)
                self.canteens_updated[canteen.siret] = canteen

            except Exception as e:
                identifier = row[self.siret_idx] if row else None
                for error in self._parse_errors(e, row, identifier):
                    self.errors.append(self._get_error(e, error["message"], error["code"], row_number))

    @transaction.atomic
    def _save_data_from_row(self, row):
        """Process and save canteen data from row"""
        (
            import_source,
            silently_added_manager_emails,
        ) = self._generate_canteen_meta_fields(row)
        canteen = self._update_canteen(row, import_source, silently_added_manager_emails)

        return canteen

    def _get_manager_emails(self, row):
        manager_emails = row.split(",")
        normalized_emails = list(map(lambda x: get_user_model().objects.normalize_email(x.strip()), manager_emails))
        for email in normalized_emails:
            validate_email(email)
        return normalized_emails

    def _add_managers_to_canteen(self, emails, canteen):
        for email in emails:
            try:
                AddManagerView.add_manager_to_canteen(email, canteen, send_invitation_mail=False)
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

    def _update_canteen(
        self,
        row,
        import_source,
        silently_added_manager_emails,
    ):
        siret = utils_utils.normalize_string(row[self.siret_idx])
        canteen_exists = Canteen.objects.filter(siret=siret).exists()

        if not canteen_exists:
            raise ValidationError({"siret": f"Aucune cantine avec le SIRET {siret} trouvée sur la plateforme."})

        canteen = Canteen.objects.get(siret=siret)
        canteen.import_source = import_source
        canteen.save(skip_validations=True)
        update_change_reason(canteen, f"Mass CSV import. {self.__class__.__name__[:100]}")
        self._add_managers_to_canteen(silently_added_manager_emails, canteen)
        return canteen

    def _generate_canteen_meta_fields(self, row):
        silently_added_manager_emails = []
        import_source = row[self.source_idx].strip()
        try:
            silently_added_manager_emails = self._get_manager_emails(row[self.silent_manager_idx])
        except Exception:
            raise ValidationError(
                {
                    "email": f"Un adresse email des gestionnaires (pas notifiés) ({row[self.silent_manager_idx]}) n'est pas valide."
                }
            )
        return (import_source, silently_added_manager_emails)

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
