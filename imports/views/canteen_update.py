from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError, transaction
from rest_framework.exceptions import PermissionDenied
from simple_history.utils import update_change_reason
from django.utils import timezone

from api.serializers import FullCanteenSerializer
from imports.models import ImportSchema, ImportType
from imports.views.base import BaseImportView
from common.utils import utils as utils_utils
from data.models import Canteen, Sector
from data.models.diagnostic_teledeclaration_dates import is_in_teledeclaration_or_correction

from api.views.canteen_managers import AddManagerView
from common.utils.camelize import camelize


CANTEEN_UPDATE_SCHEMA = ImportSchema("cantines_modifier.json")


class CanteensUpdateImportView(BaseImportView):
    import_type = ImportType.CANTEEN_UPDATE
    model_class = Canteen

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.canteens_updated = {}

    def _get_schema(self):
        return CANTEEN_UPDATE_SCHEMA

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
        row_dict = self._get_row_dict(row)
        manager_emails = self._get_manager_emails_to_notify(row_dict)
        canteen = self._update_canteen(row_dict, manager_emails)
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

    def _get_canteen_ids(self):
        return {canteen.id for canteen in self.canteens_updated.values()}

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

    def _get_manager_emails_to_notify(self, row_dict):
        try:
            manager_emails = []
            if row_dict.get("gestionnaires_additionnels"):
                manager_emails = CanteensUpdateImportView._get_manager_emails(row_dict["gestionnaires_additionnels"])
        except Exception:
            raise ValidationError(
                {
                    "email": f"Un adresse email des gestionnaires ({row_dict['gestionnaires_additionnels']}) n'est pas valide."
                }
            )
        return manager_emails

    def _update_canteen(
        self,
        row_dict,
        manager_emails,
    ):
        id = row_dict["cantine_id"]

        # ID : check canteen exists
        canteen = Canteen.objects.get(id=id)
        if not canteen:
            raise ValidationError(
                {"id": f"Aucune cantine avec le numéro identifiant « {id} » trouvée sur la plateforme."}
            )

        siret = utils_utils.normalize_string(row_dict["siret"]) if row_dict["siret"] else None
        siren_unite_legale = (
            utils_utils.normalize_string(row_dict["siren_unite_legale"]) if row_dict["siren_unite_legale"] else None
        )
        name = row_dict["nom"].strip()

        city_insee_code = utils_utils.normalize_string(row_dict["code_insee"]) if row_dict["code_insee"] else None
        # Validate city_insee_code
        if siren_unite_legale:
            if not city_insee_code:
                raise ValidationError(
                    {
                        "city_insee_code": "Le code INSEE est obligatoire pour les cantines avec le 'siren_unite_legale' de renseigné."
                    }
                )
            elif len(city_insee_code) != 5:
                raise ValidationError(
                    {
                        "city_insee_code": f"Le code INSEE « {city_insee_code} » n'est pas valide, il doit contenir 5 caractères (ex : 75056)."
                    }
                )

        central_producer_siret = (
            utils_utils.normalize_string(row_dict["siret_cuisine_centrale"])
            if row_dict["siret_cuisine_centrale"]
            else None
        )
        daily_meal_count = row_dict["nombre_repas_jour"]
        yearly_meal_count = row_dict["nombre_repas_an"]
        sector_list = [
            next(value for value, label in Sector.choices if label == sector.strip().replace("’", "'"))
            for sector in row_dict["secteurs"].strip().split(",")
        ]
        production_type = next(
            (
                value
                for value, label in Canteen.ProductionType.choices
                if row_dict["type_production"].strip() in [label, value]
            ),
            None,
        )
        management_type = next(
            (
                value
                for value, label in Canteen.ManagementType.choices
                if row_dict["type_gestion"].strip() in [label, value]
            ),
            None,
        )
        economic_model = next(
            (
                value
                for value, label in Canteen.EconomicModel.choices
                if row_dict["modèle_économique"].strip() in [label, value]
            ),
            None,
        )

        # Group custom validation
        groupe_id = row_dict["groupe_id"]
        groupe = None
        # Group exists
        if groupe_id:
            try:
                groupe = Canteen.objects.get(id=groupe_id)
            except Exception:
                raise ValidationError(
                    {"groupe_id": f"Aucun groupe avec le numéro identifiant « {groupe_id} » trouvé sur la plateforme."}
                )
        # Group did not teledeclare already
        last_year = timezone.now().year - 1
        if groupe and is_in_teledeclaration_or_correction():
            has_diagnostic_teledeclared_for_year = groupe.has_diagnostic_teledeclared_for_year(last_year)
            if has_diagnostic_teledeclared_for_year:
                raise ValidationError(
                    {
                        "groupe_id": f"Vous ne pouvez pas ajouter de restaurant satellite au groupe « {groupe_id} », car il possède un bilan télédéclaré (campagne de télédéclaration en cours). Veuillez annuler la télédéclaration pour pouvoir ajouter le(s) restaurant(s) satellite(s)."
                    }
                )

        line_ministry = (
            next(
                (
                    value
                    for value, label in Canteen.Ministries.choices
                    if label == row_dict["administration_tutelle"].strip()
                ),
                None,
            )
            if row_dict["administration_tutelle"]
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
